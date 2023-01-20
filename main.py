from fastapi import FastAPI
from survivors.routers import survivors_routers
from exceptions import IdNotFound, id_not_found_exception_handler, CoordinatesOutOfRange, coordinates_out_of_range_exception_handler


app = FastAPI()

@app.get("/")
async def root():
    return "[Latitude.sh] Maxihost - Backend test by Eduardo Lima"
    
app.include_router(survivors_routers.router)
app.add_exception_handler(IdNotFound, id_not_found_exception_handler)
app.add_exception_handler(CoordinatesOutOfRange, coordinates_out_of_range_exception_handler)



# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8001)