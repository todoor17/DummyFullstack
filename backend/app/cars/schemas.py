from typing import Optional

from pydantic import BaseModel, Field


class CarBase(BaseModel):
    id: int = Field(description="Car ID", gt=0)
    brand: str = Field(description="Brand Name")
    mileage: int = Field(description="Car Mileage")
    nr_of_seats: int = Field(default=0)
    car_color: str = Field(description="Car Color")
    owner: int = Field(description="Owner ID")

    class Config:
        orm_mode = True

class CreateCarRequest(BaseModel):
    brand: str = Field(description="Brand Name")
    mileage: int = Field(description="Car Mileage")
    nr_of_seats: Optional[int] = Field(default=0)
    car_color: str = Field(description="Car Color")
    owner: int = Field(description="Owner ID")