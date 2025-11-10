from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..database import get_db
from ..dependencies import verify_api_key

router = APIRouter(prefix="/buildings", tags=["Buildings"])


@router.get("/", response_model=List[schemas.Building])
def get_buildings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    return crud.get_buildings(db, skip=skip, limit=limit)
