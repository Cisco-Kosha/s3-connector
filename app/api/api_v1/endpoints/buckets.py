from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, FastAPI, File
from starlette.responses import JSONResponse

from app import schemas
from app.crud import crud_bucket
from app.api.api_v1 import deps

router = APIRouter()


@router.get("/", response_model=List[Any])
def list_objects(file: Optional[str] = None, bucket=Depends(crud_bucket.CRUDBucket)) -> Any:
    if file:
        obj = bucket.load(file)
        return JSONResponse(obj)
    else:
        objects = bucket.list_ids()
        return objects


@router.post("/", response_model=List[Any])
def save_object(prefix: str, file: UploadFile = File(...), bucket=Depends(crud_bucket.CRUDBucket)) -> Any:
    print(file)
    filename = file.filename
    if prefix:
        filename = prefix + "/" + file.filename
    bucket.save(file, filename)
    return JSONResponse({"status": "success"})


@router.delete("/{file}", response_model=List[Any])
def delete_object(file: str, bucket=Depends(crud_bucket.CRUDBucket)) -> Any:
    res = bucket.delete_obj(file)
    return JSONResponse(res)
