from typing import Any, List, Optional

import boto3
from fastapi import APIRouter, Depends, HTTPException

from fastapi.responses import JSONResponse

from fastapi import Request

router = APIRouter()


@router.get("/", response_model=Any)
def get_connector_spec():
    return JSONResponse({"AWS_SERVER_SECRET_KEY": "Secret access key", "AWS_SERVER_PUBLIC_KEY": "Access key Iid"})


@router.post("/check", response_model=Any)
async def check_connector_spec(request: Request):
    data = await request.json()
    if data is not None:
        s3 = boto3.resource('s3', aws_access_key_id=data["AWS_SERVER_PUBLIC_KEY"],
              aws_secret_access_key=data["AWS_SERVER_SECRET_KEY"])
        buckets = [bucket.name for bucket in s3.buckets.all()]
        if buckets is not None:
            return True
        else:
            return False
    else:
        return False
