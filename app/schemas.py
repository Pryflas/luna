from pydantic import BaseModel, Field
from typing import List, Optional


class PhoneNumberBase(BaseModel):
    number: str


class PhoneNumberCreate(PhoneNumberBase):
    pass


class PhoneNumber(PhoneNumberBase):
    id: int
    organization_id: int

    class Config:
        from_attributes = True


class BuildingBase(BaseModel):
    address: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class BuildingCreate(BuildingBase):
    pass


class Building(BuildingBase):
    id: int

    class Config:
        from_attributes = True


class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class ActivityCreate(ActivityBase):
    pass


class Activity(ActivityBase):
    id: int
    level: int

    class Config:
        from_attributes = True


class ActivityTree(Activity):
    children: List["ActivityTree"] = []

    class Config:
        from_attributes = True


class OrganizationBase(BaseModel):
    name: str
    building_id: int


class OrganizationCreate(OrganizationBase):
    phone_numbers: List[str]
    activity_ids: List[int]


class Organization(OrganizationBase):
    id: int
    phone_numbers: List[PhoneNumber] = []
    activities: List[Activity] = []
    building: Building

    class Config:
        from_attributes = True
