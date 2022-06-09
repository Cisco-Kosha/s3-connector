from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, FastAPI, File
from starlette.responses import JSONResponse

from app.crud import crud_bucket
from botocore.exceptions import ClientError

from app.utils import exception

router = APIRouter()


@router.get("/{bucket_id}", response_model=List[Any])
def list_objects_in_a_bucket(bucket_id: str, file: Optional[str] = None, bucket=Depends(crud_bucket.CRUDBucket)) -> Any:
    if file:
        try:
            (obj, err) = bucket.load(bucket_id, file)
        except exception.NoSuchFileExists as e:
            return JSONResponse(status_code=404, content=str(e))
        else:
            return JSONResponse(obj)
    else:
        try:
            objects, err = bucket.list_ids(bucket_id)
        except exception.NoSuchBucketExists as e:
            return JSONResponse(status_code=404, content=str(e))
        return objects


@router.get("/", response_model=List[Any])
def list_all_buckets() -> Any:
    obj = crud_bucket.list_all_buckets()
    return JSONResponse(obj)


@router.post("/{bucket_id}", response_model=List[Any])
def save_object_in_a_bucket(bucket_id: str, prefix: str, file: UploadFile = File(...), bucket=Depends(crud_bucket.CRUDBucket)) -> Any:
    print(file)
    filename = file.filename
    if prefix:
        filename = prefix + "/" + file.filename
    res = bucket.save(bucket_id, file, filename)
    return JSONResponse(res)


@router.put("/{bucket_name}", response_model=List[Any])
def create_s3_bucket(bucket_name: str, region: str, bucket=Depends(crud_bucket.CRUDBucket)) -> Any:
    if region:
        try:
            res = bucket.create(bucket_name, region)
        except ClientError as e:
            return JSONResponse(status_code=400, content=str(e))
        return JSONResponse({"result": "success"})
    else:
        return JSONResponse(status_code=400, content="Region must be specified")


@router.delete("/{bucket_id}", response_model=List[Any])
def delete_object_in_a_bucket(bucket_id: str, file: str = None, bucket=Depends(crud_bucket.CRUDBucket)) -> Any:
    if not file:
        return JSONResponse("file query parameter needs to be set")
    res = bucket.delete_obj(bucket_id, file)
    return JSONResponse(res)
