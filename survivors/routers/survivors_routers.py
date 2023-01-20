from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from survivors.models.survivors_model import Survivor
from haversine import haversine
from typing import List, Optional
from exceptions import IdNotFound

router = APIRouter(prefix="/survivors")

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


@router.get("", response_model=List[SurvivorResponse] )
async def get_all_survivors(db: Session = Depends(get_db)) -> List[SurvivorResponse]:

    return db.query(Survivor).all()


@router.get("/{id_survivor}", response_model= Optional[SurvivorResponse])
async def get_survivor_by_id(id_survivor: int, db: Session = Depends(get_db)) -> SurvivorResponse:

    survivor_request = get_survivor_by_id(id_survivor, db)

    return survivor_request


@router.get("/distances/{id_survivor}", response_model=SurvivorResponse)
async def get_closest_survivor(id_survivor: int, db: Session = Depends(get_db)) -> SurvivorResponse:

    survivor_request = get_survivor_by_id(id_survivor, db)
    lat_reference = survivor_request.latitude
    long_reference = survivor_request.longitude
    all_survivors = db.query(Survivor).all()
    distances = get_distances_from_survivor(id_survivor, all_survivors, lat_reference, long_reference)

    closest_survivor = db.query(Survivor).get(min(distances, key=distances.get))

    return closest_survivor


@router.patch("/{id_survivor}", response_model=SurvivorResponse)
async def mark_as_infected(id_survivor: int, db: Session = Depends(get_db)) -> SurvivorResponse:

    survivor_to_mark = get_survivor_by_id(id_survivor, db)
    survivor_to_mark.reported_infected  += 1
    
    if survivor_to_mark.reported_infected >= 3:
        survivor_to_mark.infected = True
    
    db.add(survivor_to_mark)
    db.commit()
    db.refresh(survivor_to_mark)

    return survivor_to_mark


@router.post("", response_model= SurvivorResponse, status_code= 201)
async def create_survivor(survivor_request: SurvivorRequest, db: Session = Depends(get_db)) -> SurvivorResponse:

    survivor_to_create = Survivor(**survivor_request.dict()) 

    db.add(survivor_to_create)
    db.commit()
    db.refresh(survivor_to_create)

    return survivor_to_create


@router.put("/{id_survivor}", response_model= SurvivorResponse, status_code= 200)
async def update_survivor(id_survivor: int, survivor_request: SurvivorRequest, db: Session = Depends(get_db)) -> SurvivorResponse:

    survivor_to_update = get_survivor_by_id(id_survivor, db)
    survivor_to_update.name = survivor_request.name
    survivor_to_update.gender = survivor_request.gender
    survivor_to_update.latitude = survivor_request.latitude
    survivor_to_update.longitude = survivor_request.longitude

    db.add(survivor_to_update)
    db.commit()
    db.refresh(survivor_to_update)

    return survivor_to_update


def get_distances_from_survivor(id_survivor: int, list_survivors: List, lat_reference: float, long_reference: float) -> dict:

    distances = {}
    for survivor in list_survivors:
        if survivor.id != id_survivor:
            distance = haversine((lat_reference, long_reference), (survivor.latitude,survivor.longitude)) 
            distances[survivor.id] = distance

    return distances


def get_survivor_by_id(id_survivor: int, db: Session = Depends(get_db)) -> Survivor:

    survivor_request = db.query(Survivor).get(id_survivor)
    
    if survivor_request is None:
        raise IdNotFound(id_survivor)

    return survivor_request