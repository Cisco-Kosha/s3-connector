from fastapi import APIRouter

from app.api.api_v1.endpoints import buckets

api_router = APIRouter()

api_router.include_router(buckets.router, prefix="/s3/buckets", tags=["buckets"])
