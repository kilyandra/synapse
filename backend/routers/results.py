from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from benchmarks import is_better
from database import get_db
from models import User, Result, BestResult
from schemas import ResultCreate
from auth import get_current_user

router = APIRouter(prefix="/results", tags=["results"])


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
def create_result(
    data: ResultCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = Result(
        user_id=current_user.id,
        benchmark=data.benchmark,
        score=data.score,
    )
    db.add(result)

    best = (
        db.query(BestResult)
        .filter(
            BestResult.user_id == current_user.id,
            BestResult.benchmark == data.benchmark,
        )
        .first()
    )

    if best is None:
        best = BestResult(
            user_id=current_user.id,
            benchmark=data.benchmark,
            score=data.score,
        )
        db.add(best)
    elif is_better(data.benchmark, data.score, best.score):
        best.score = data.score
        best.updated_at = datetime.now(timezone.utc)

    db.commit()


@router.get("/best")
def get_my_best(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    bests = (
        db.query(BestResult)
        .filter(BestResult.user_id == current_user.id)
        .all()
    )
    return [
        {"benchmark": b.benchmark, "score": b.score}
        for b in bests
    ]
