from fastapi import APIRouter
from core.config import settings
from api.router.df_router import router as df_router

router = APIRouter(
    prefix=settings.api.v1.prefix
)

router.include_router(df_router)
