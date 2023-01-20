from fastapi import Request
from fastapi.responses import JSONResponse

class IdNotFound(Exception):
    def __init__(self, name: str):
        self.name = name

async def id_not_found_exception_handler(request: Request, exc: IdNotFound):
    return JSONResponse(
        status_code= 404,
        content= {"message": f"Survivor Id '{exc.name}' not found"},
    )

