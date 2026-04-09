from fastapi import FastAPI

from plippy.api.v1.health import router as health_router
from plippy.api.v1.orchestrations import router as orchestrations_router
from plippy.api.v1.users import router as users_router


app = FastAPI(title="plippy API")
app.include_router(health_router)
app.include_router(orchestrations_router)
app.include_router(users_router)
