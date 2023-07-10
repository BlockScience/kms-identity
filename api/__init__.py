from fastapi import FastAPI
from api.routers import objects, identity

app = FastAPI()

app.include_router(objects.router)