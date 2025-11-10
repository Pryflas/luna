from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from . import models, schemas
import math


def get_organization(db: Session, organization_id: int):
    return (
        db.query(models.Organization)
        .filter(models.Organization.id == organization_id)
        .first()
    )


def get_organizations_by_building(db: Session, building_id: int):
    return (
        db.query(models.Organization)
        .filter(models.Organization.building_id == building_id)
        .all()
    )


def get_organizations_by_activity(db: Session, activity_id: int):
    activity = (
        db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    )
    if not activity:
        return []

    activity_ids = [activity_id]

    def get_children_ids(parent_id: int):
        children = (
            db.query(models.Activity)
            .filter(models.Activity.parent_id == parent_id)
            .all()
        )
        for child in children:
            activity_ids.append(child.id)
            get_children_ids(child.id)

    get_children_ids(activity_id)

    return (
        db.query(models.Organization)
        .join(models.organization_activity)
        .filter(models.organization_activity.c.activity_id.in_(activity_ids))
        .distinct()
        .all()
    )


def get_organizations_by_radius(
    db: Session, latitude: float, longitude: float, radius_km: float
):
    R = 6371

    organizations = db.query(models.Organization).join(models.Building).all()
    result = []

    for org in organizations:
        lat1, lon1 = math.radians(latitude), math.radians(longitude)
        lat2, lon2 = math.radians(org.building.latitude), math.radians(
            org.building.longitude
        )

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))
        distance = R * c

        if distance <= radius_km:
            result.append(org)

    return result


def get_organizations_by_rectangle(
    db: Session, lat1: float, lon1: float, lat2: float, lon2: float
):
    min_lat, max_lat = min(lat1, lat2), max(lat1, lat2)
    min_lon, max_lon = min(lon1, lon2), max(lon1, lon2)

    return (
        db.query(models.Organization)
        .join(models.Building)
        .filter(
            and_(
                models.Building.latitude >= min_lat,
                models.Building.latitude <= max_lat,
                models.Building.longitude >= min_lon,
                models.Building.longitude <= max_lon,
            )
        )
        .all()
    )


def search_organizations_by_name(db: Session, name: str):
    return (
        db.query(models.Organization)
        .filter(models.Organization.name.ilike(f"%{name}%"))
        .all()
    )


def get_buildings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Building).offset(skip).limit(limit).all()


def create_activity(db: Session, activity: schemas.ActivityCreate):
    level = 1
    if activity.parent_id:
        parent = (
            db.query(models.Activity)
            .filter(models.Activity.id == activity.parent_id)
            .first()
        )
        if parent:
            level = parent.level + 1
            if level > 3:
                raise ValueError("Превышен максимальный уровень вложенности (3)")

    db_activity = models.Activity(
        name=activity.name, parent_id=activity.parent_id, level=level
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity
