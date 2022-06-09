from fastapi import APIRouter

from app.api.api_v1.endpoints import connector

spec_router = APIRouter()

spec_router.include_router(connector.router, prefix="/s3/spec", tags=["connector spec endpoints"])


