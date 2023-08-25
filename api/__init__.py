from .core import *
from .routers import *
from . import config
from . import database
from . import exceptions
from . import queries
from . import schema
from . import utils

from fastapi import FastAPI

app = FastAPI()

app.include_router(objects.router)