from fastapi import FastAPI
from survivors.routers import survivors_routers
from fastapi.responses import RedirectResponse
from exceptions import IdNotFound, id_not_found_exception_handler, CoordinatesOutOfRange, coordinates_out_of_range_exception_handler

description = """
SurvivosAPI is an API that helps you locate other survivors. 

## Survivors

You will be able to:

* **Get all survivors** 
* **Create a survivor** 
* **Get a survivor by id** 
* **Update a survivor** 
* **Report a survivor as infected** 
* **Get the closest survivor from a survivor** 



Developed by: **Eduardo Lima**
"""
app = FastAPI(title="SurvivorsAPI",
    description=description,
    version="0.0.1",
    contact={
        "email": "lima.edu.araujo@gmail.com",
    },
    )

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url = '/survivors')
    
app.include_router(survivors_routers.router)
app.add_exception_handler(IdNotFound, id_not_found_exception_handler)
app.add_exception_handler(CoordinatesOutOfRange, coordinates_out_of_range_exception_handler)



# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8001)