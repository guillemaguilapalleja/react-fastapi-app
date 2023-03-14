from fastapi import APIRouter, Depends, HTTPException, status
from schemas import SortMapSchema, ResponseSchema, RequestSchema
from sqlalchemy.orm import Session
from database import get_db
import crud
from exceptions import (
    SortMapNotFoundException,
    SortMapValueNotValidException,
    MessageToEncryptNotValidException,
)
import time

router = APIRouter(prefix="/api")


@router.post("/sortmap", status_code=status.HTTP_201_CREATED)
def create_sortmap(sortmap: SortMapSchema, db: Session = Depends(get_db)):
    try:
        if not sortmap.value.isdigit():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A SortMap must be a string of digits only (0123456789)",
            )
        return crud.create_sortmap(sortmap=sortmap, db=db)
    except SortMapValueNotValidException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A SortMap can not have duplicates numbers in it",
        )


@router.get("/sortmaps_list")
def get_sortmaps_list(db: Session = Depends(get_db)):
    return crud.get_sortmaps_list(db=db)


@router.get("/sortmaps")
def get_sortmap_by_id(sortmap_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_sortmap_by_id(sortmap_id=sortmap_id, db=db)
    except SortMapNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no SortMap with id={sortmap_id}",
        )


@router.put("/sortmap/{sortmap_id}")
def update_sortmap(
    sortmap_id: int, sortmap_value: SortMapSchema, db: Session = Depends(get_db)
):
    try:
        return crud.update_sortmap(sortmap_value=sortmap_value, id=sortmap_id, db=db)
    except SortMapNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no SortMap with id={sortmap_id}",
        )
    except SortMapValueNotValidException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )


@router.delete("/sortmap/{sortmap_id}")
def delete_sortmap(sortmap_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_sortmap(sortmap_id=sortmap_id, db=db)
    except SortMapNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no SortMap with id={sortmap_id}",
        )


@router.post("/order")
def encrypt_message(
    sortmap_id: int, message_to_encrypt: RequestSchema, db: Session = Depends(get_db)
):
    try:
        starting_time = time.time()
        message_encrypted = crud.encrypt_message(
            message_to_encrypt=message_to_encrypt.request, sortmap_id=sortmap_id, db=db
        )
        finishing_time = time.time()
        total_time = finishing_time - starting_time
        return ResponseSchema(
            sortmap_id=sortmap_id, response=message_encrypted, time=total_time * 1000
        )
    except SortMapNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no SortMap with id={sortmap_id}",
        )
