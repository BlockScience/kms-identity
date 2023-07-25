from fastapi import FastAPI
from api.routers import objects, relations, assertions

app = FastAPI()

app.include_router(objects.router)
app.include_router(relations.router)
app.include_router(assertions.router)