from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, crud
from ..database import get_db
from ..dependencies import verify_api_key

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/{organization_id}", response_model=schemas.Organization)
def get_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    org = crud.get_organization(db, organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return org


@router.get("/", response_model=List[schemas.Organization])
def get_organizations(
    building_id: Optional[int] = Query(None, description="ID здания"),
    activity_id: Optional[int] = Query(None, description="ID вида деятельности"),
    name: Optional[str] = Query(None, description="Название организации"),
    latitude: Optional[float] = Query(None, description="Широта точки"),
    longitude: Optional[float] = Query(None, description="Долгота точки"),
    radius_km: Optional[float] = Query(None, description="Радиус в км"),
    lat1: Optional[float] = Query(
        None, description="Широта первого угла прямоугольника"
    ),
    lon1: Optional[float] = Query(
        None, description="Долгота первого угла прямоугольника"
    ),
    lat2: Optional[float] = Query(
        None, description="Широта второго угла прямоугольника"
    ),
    lon2: Optional[float] = Query(
        None, description="Долгота второго угла прямоугольника"
    ),
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    if building_id:
        return crud.get_organizations_by_building(db, building_id)

    if activity_id:
        return crud.get_organizations_by_activity(db, activity_id)

    if name:
        return crud.search_organizations_by_name(db, name)

    if latitude is not None and longitude is not None and radius_km is not None:
        return crud.get_organizations_by_radius(db, latitude, longitude, radius_km)

    if all(v is not None for v in [lat1, lon1, lat2, lon2]):
        return crud.get_organizations_by_rectangle(db, lat1, lon1, lat2, lon2)

    raise HTTPException(
        status_code=400, detail="Необходимо указать параметры фильтрации"
    )
