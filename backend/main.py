import logging
from fastapi import FastAPI, APIRouter, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from config import RATE_LIMIT_DEFAULT, Errors
from database import Base, engine
from limiter import limiter
import models  # noqa: F401
from routers import auth as auth_router
from routers import results as results_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Synapse API",
    docs_url="/api",
    redoc_url=None,
    openapi_url="/api/openapi.json",
)

app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    logger.warning(f"rate limit exceeded on {request.url.path} by {get_remote_address(request)}")
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": Errors.TOO_MANY_REQUESTS},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"validation error on {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": Errors.INVALID_INPUT},
    )


api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router.router)
api_router.include_router(results_router.router)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
@limiter.limit(RATE_LIMIT_DEFAULT)
def root(request: Request):
    return {"status": "ok"}
