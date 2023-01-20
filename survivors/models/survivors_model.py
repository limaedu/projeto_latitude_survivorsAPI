from database import Base
from sqlalchemy import Boolean, Column, Integer, String, Float
from pydantic import BaseModel

class Survivor(Base):
    __tablename__ = 'survivors'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    gender = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    infected = Column(Boolean, default=False)
    reported_infected = Column(Integer, default=0)


class SurvivorResponse(BaseModel):
    id: int
    name: str
    gender: str
    latitude: float
    longitude: float
    infected: bool

    class Config:
        orm_mode = True


class SurvivorRequest(BaseModel):
    name: str
    gender: str
    latitude: float
    longitude: float
