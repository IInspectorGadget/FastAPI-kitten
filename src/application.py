import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from src.api.breed import router as breed_router
from src.api.kitten import router as kitten_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    logger.info(f"Start")
    yield
    # Shutdown



def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(kitten_router)
    app.include_router(breed_router)
    return app

app = create_app()

@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request, exc: IntegrityError):
    detail_message = str(exc.orig)
    if "ForeignKeyViolationError" in detail_message:
        detail_part = detail_message.split("DETAIL:")[1]
        detail_message = detail_part.strip()
        return JSONResponse(
            status_code=400,
            content={"detail": detail_message}
        )
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."}
    )
