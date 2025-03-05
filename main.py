import logging
import platform
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import router
from core.config import settings
from core.models.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = logging.getLogger("uvicorn")
    current_os = platform.system()
    if current_os == "Windows":
        logger.info(f"Documentation: http://{settings.run.host}:{settings.run.port}/docs")
    if current_os == "Linux":
        logger.info(f"Documentation: http://{settings.run.host}:8001/docs")
    yield
    db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)
main_app.include_router(router,
                        prefix=settings.api.prefix)
if __name__ == '__main__':
    uvicorn.run("main:main_app", host=settings.run.host, port=settings.run.port, reload=True)
