from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint

from app.database import Base

class Car(Base):
    __tablename__ = "cars"

    id: int = Column(Integer, primary_key=True, index=True)
    brand: str = Column(String(50))
    mileage: int = Column(Integer)
    nr_of_seats: int = Column(Integer, default=0)
    car_color: str = Column(String(20))
    owner: id = Column(Integer, ForeignKey("users.id"))

    __table_args__ = (
        CheckConstraint("mileage >= 0 AND mileage <= 999999", name="mileage_range"),
    )

