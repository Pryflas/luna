from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..database import get_db
from ..dependencies import verify_api_key

router = APIRouter(prefix="/activities", tags=["Activities"])


@router.get("/", response_model=List[schemas.Activity])
def get_activities(
    db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)
):
    return db.query(crud.models.Activity).all()
