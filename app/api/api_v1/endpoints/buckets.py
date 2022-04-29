from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, FastAPI, File
from starlette.responses import JSONResponse

from app import schemas
from app.crud import crud_bucket
from app.api.api_v1 import deps

router = APIRouter()


@router.get("/{bucket_id}", response_model=List[Any])
def list_objects(bucket_id: str, file: Optional[str] = None, bucket=Depends(crud_bucket.CRUDBucket)) -> Any:
    if file:
        obj = bucket.load(bucket_id, file)
        return JSONResponse(obj)
    else:
        objects = bucket.list_ids(bucket_id)
        return objects


@router.post("/{bucket_id}", response_model=List[Any])
def save_object(bucket_id: str, prefix: str, file: UploadFile = File(...), bucket=Depends(crud_bucket.CRUDBucket)) -> Any:
    print(file)
    filename = file.filename
    if prefix:
        filename = prefix + "/" + file.filename
    bucket.save(bucket_id, file, filename)
    return JSONResponse({"status": "success"})


@router.delete("/{bucket_id}/{file}", response_model=List[Any])
def delete_object(bucket_id: str, file: str, bucket=Depends(crud_bucket.CRUDBucket)) -> Any:
    res = bucket.delete_obj(bucket_id, file)
    return JSONResponse(res)
