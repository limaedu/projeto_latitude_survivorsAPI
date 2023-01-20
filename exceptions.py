from fastapi import Request
from fastapi.responses import JSONResponse


class IdNotFound(Exception):
    def __init__(self, name: str):
        self.name = name

class CoordinatesOutOfRange(Exception):
    pass

async def id_not_found_exception_handler(request: Request, exc: IdNotFound):
    return JSONResponse(
        status_code= 404,
        content= {"message": f"Survivor Id '{exc.name}' not found"},
    )

async def coordinates_out_of_range_exception_handler(request: Request, exc: CoordinatesOutOfRange):
    return JSONResponse(
        status_code= 400,
        content= {"message": f"Coordinates are out of range. Latitude must be a value between [-90,90] and Longitude between [-180,180]"},
        
    )

