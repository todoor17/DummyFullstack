from fastapi import FastAPI

from app import cars
from app.database import engine, Base
from app.users.routers import create_user, delete_user, get_all_users, get_user, update_user, login
from app.cars.routers import create_car

from app.cars.model import Car
from app.users.model import User

app = FastAPI()

Base.metadata.create_all(engine)

# USERS
app.include_router(create_user.router)
app.include_router(delete_user.router)
app.include_router(get_all_users.router)
app.include_router(get_user.router)
app.include_router(update_user.router)

app.include_router(login.router)

# CARS
app.include_router(create_car.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

