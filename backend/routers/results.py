from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from benchmarks import is_better
from config import RATE_LIMIT_DEFAULT
from database import get_db
from limiter import limiter
from models import User, Result, BestResult
from schemas import ResultCreate
from auth import get_current_user

router = APIRouter(prefix="/results", tags=["results"])


def _record_result(db: Session, user: User, benchmark: str, score: int) -> None:
    db.add(Result(user_id=user.id, benchmark=benchmark, score=score))

    best = (
        db.query(BestResult)
        .filter(BestResult.user_id == user.id, BestResult.benchmark == benchmark)
        .first()
    )

    if best is None:
        db.add(BestResult(user_id=user.id, benchmark=benchmark, score=score))
    elif is_better(benchmark, score, best.score):
        best.score = score
        best.updated_at = datetime.now(timezone.utc)


def _best_results(db: Session, user: User) -> list[dict]:
    bests = db.query(BestResult).filter(BestResult.user_id == user.id).all()
    return [{"benchmark": b.benchmark, "score": b.score} for b in bests]


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(RATE_LIMIT_DEFAULT)
def create_result(
        request: Request,
        data: ResultCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    _record_result(db, current_user, data.benchmark, data.score)
    db.commit()


@router.post("/check")
@limiter.limit(RATE_LIMIT_DEFAULT)
def check_results(
        request: Request,
        data: list[ResultCreate],
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    for item in data:
        _record_result(db, current_user, item.benchmark, item.score)
    db.commit()

    return _best_results(db, current_user)


@router.get("/best")
@limiter.limit(RATE_LIMIT_DEFAULT)
def get_my_best(
        request: Request,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    return _best_results(db, current_user)
