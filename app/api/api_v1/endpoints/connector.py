from typing import Any, List, Optional

import boto3
from fastapi import APIRouter, Depends, HTTPException

from fastapi.responses import JSONResponse

from fastapi import Request

router = APIRouter()


@router.get("/list", response_model=Any)
def get_connector_spec():
    return JSONResponse({"AWS_SECRET_ACCESS_KEY": "AWS Secret Access Key", "AWS_ACCESS_KEY_ID": "AWS Access Key Id"})


@router.post("/test", response_model=Any)
async def check_connector_spec(request: Request):
    data = await request.json()
    if data is not None:
        s3 = boto3.resource('s3', aws_access_key_id=data["AWS_ACCESS_KEY_ID"],
                            aws_secret_access_key=data["AWS_SECRET_ACCESS_KEY"])
        buckets = [bucket.name for bucket in s3.buckets.all()]
        if buckets is not None:
            return True
        else:
            return False
    else:
        return False
