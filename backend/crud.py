from typing import List

from sqlalchemy import Row
from sqlalchemy.orm import Session
from models import SortMaps
from schemas import SortMapSchema
from exceptions import SortMapNotFoundException, SortMapValueNotValidException


def get_sortmap_by_value(value: str, db: Session) -> Row[SortMaps]:
    db_sortmap = db.query(SortMaps).filter(SortMaps.value == value).first()
    if not db_sortmap:
        raise SortMapNotFoundException()
    return db_sortmap


def get_sortmap_by_id(sortmap_id: int, db: Session) -> Row[SortMaps]:
    db_sortmap = db.query(SortMaps).filter(SortMaps.id == sortmap_id).first()
    if not db_sortmap:
        raise SortMapNotFoundException()
    return db_sortmap


def create_sortmap(sortmap: SortMapSchema, db: Session) -> Row[SortMaps]:
    x = []
    for i in sortmap.value:
        if i not in x and sortmap.value.count(i) > 1:
            x.append(i)
    if len(x) > 0 or not sortmap.value.isdigit():
        raise SortMapValueNotValidException()
    db_sortmap = SortMaps(value=sortmap.value)
    db.add(db_sortmap)
    db.commit()
    return get_sortmap_by_value(value=sortmap.value, db=db)


def get_sortmaps_list(db: Session) -> List[SortMaps]:
    return db.query(SortMaps).all()


def update_sortmap(sortmap_value: SortMapSchema, id: int, db: Session) -> Row[SortMaps]:
    if not sortmap_value.value.isdigit():
        raise SortMapValueNotValidException()
    db_sortmap = get_sortmap_by_id(sortmap_id=id, db=db)
    db_sortmap.value = sortmap_value.value
    db.commit()
    return get_sortmap_by_value(value=sortmap_value.value, db=db)


def delete_sortmap(sortmap_id: int, db: Session) -> None:
    db_sortmap = get_sortmap_by_id(sortmap_id=sortmap_id, db=db)
    db.delete(db_sortmap)
    db.commit()


def encrypt_message(message_to_encrypt: str, sortmap_id: int, db: Session) -> str:
    db_sortmap = get_sortmap_by_id(sortmap_id=sortmap_id, db=db)
    sortmap_dict = {char: i for i, char in enumerate(db_sortmap.value)}
    list_message_encrypted = sorted(
        message_to_encrypt, key=lambda x: sortmap_dict.get(x, len(db_sortmap.value))
    )
    return "".join(list_message_encrypted)
