import logging
from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, Depends, HTTPException, Request, status
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from sqlalchemy.orm import Session
from config import GOOGLE_CLIENT_ID, RATE_LIMIT_SENSITIVE, RATE_LIMIT_DEFAULT, Errors
from database import get_db
from limiter import limiter
from models import User
from schemas import UserCreate, UserLogin, GoogleAuth, Token, UserOut
from auth import hash_password, verify_password, create_access_token, get_current_user
from utils import generate_username

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
@limiter.limit(RATE_LIMIT_SENSITIVE)
def register(request: Request, data: UserCreate, db: Session = Depends(get_db)):
    try:
        validate_email(data.email, check_deliverability=False)
    except EmailNotValidError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=Errors.INVALID_EMAIL)

    if len(data.password) < 8:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=Errors.PASSWORD_TOO_SHORT)

    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=Errors.EMAIL_ALREADY_REGISTERED
        )

    username = generate_username()
    # regenerate in the rare case of a collision
    while db.query(User).filter(User.username == username).first():
        username = generate_username()

    user = User(
        email=data.email,
        username=username,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id)
    return Token(access_token=token)


@router.post("/login", response_model=Token)
@limiter.limit(RATE_LIMIT_SENSITIVE)
def login(request: Request, data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not user.hashed_password or not verify_password(data.password, user.hashed_password):
        logger.warning(f"failed login attempt for {data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Errors.INVALID_CREDENTIALS,
        )

    token = create_access_token(user.id)
    return Token(access_token=token)


@router.get("/me", response_model=UserOut)
@limiter.limit(RATE_LIMIT_DEFAULT)
def get_me(request: Request, current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/config")
@limiter.limit(RATE_LIMIT_DEFAULT)
def get_auth_config(request: Request):
    return {"google_client_id": GOOGLE_CLIENT_ID}


@router.post("/google", response_model=Token)
@limiter.limit(RATE_LIMIT_SENSITIVE)
def google_auth(request: Request, data: GoogleAuth, db: Session = Depends(get_db)):
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=Errors.GOOGLE_NOT_CONFIGURED,
        )

    try:
        payload = google_id_token.verify_oauth2_token(
            data.credential, google_requests.Request(), GOOGLE_CLIENT_ID
        )
    except ValueError as e:
        logger.warning(f"google token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Errors.INVALID_GOOGLE_CREDENTIAL,
        )

    if not payload.get("email_verified"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Errors.GOOGLE_EMAIL_NOT_VERIFIED,
        )

    google_id = payload["sub"]
    email = payload["email"].lower()

    user = db.query(User).filter(User.google_id == google_id).first()

    if not user:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.google_id = google_id
            user.hashed_password = None
        else:
            username = generate_username()
            while db.query(User).filter(User.username == username).first():
                username = generate_username()

            user = User(email=email, username=username, google_id=google_id)
            db.add(user)

        db.commit()
        db.refresh(user)

    token = create_access_token(user.id)
    return Token(access_token=token)
