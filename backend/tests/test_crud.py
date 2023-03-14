import random

import pytest
from fastapi.testclient import TestClient

from backend.exceptions import SortMapNotFoundException, SortMapValueNotValidException
from backend.main import app
from backend import crud
from backend.tests.utils import (
    test_db_session,
    return_sortmap,
    return_sortmap_schema,
    return_sortmap_correct_model,
    return_message_to_encrypt,
    return_correct_sortmap_schema,
)


client = TestClient(app)


def test_get_sortmap_by_value(test_db_session, return_sortmap):
    db = test_db_session
    db.add(return_sortmap)
    db.commit()

    result = crud.get_sortmap_by_value(return_sortmap.value, db)
    assert result == return_sortmap


def test_get_sortmap_by_wrong_value(test_db_session):
    db = test_db_session
    with pytest.raises(SortMapNotFoundException):
        crud.get_sortmap_by_value("Wrong value", db)


def test_get_sortmap_by_id(test_db_session, return_sortmap):
    db = test_db_session
    db.add(return_sortmap)
    db.commit()

    result = crud.get_sortmap_by_id(return_sortmap.id, db)
    assert result == return_sortmap


def test_get_sortmap_by_wrong_id(test_db_session):
    db = test_db_session
    with pytest.raises(SortMapNotFoundException):
        crud.get_sortmap_by_value(str(random.randint(1, 10)), db)


def test_create_sortmap(test_db_session, return_correct_sortmap_schema):
    db = test_db_session
    result = crud.create_sortmap(return_correct_sortmap_schema, db)
    assert result.value == return_correct_sortmap_schema.value


def test_create_sortmap_wrong_value(test_db_session, return_sortmap):
    db = test_db_session
    return_sortmap.value = "11"
    with pytest.raises(SortMapValueNotValidException):
        crud.create_sortmap(return_sortmap, db)


def test_get_sortmaps_list(test_db_session):
    db = test_db_session
    result = crud.get_sortmaps_list(db)
    assert len(result) > 0


def test_update_sortmap(test_db_session, return_sortmap):
    db = test_db_session
    id_to_search = 1
    return_sortmap.value = "012345"
    result = crud.update_sortmap(return_sortmap, id_to_search, db)
    assert result.id == id_to_search


def test_update_sortmap_wrong_new_value(test_db_session, return_sortmap_schema):
    db = test_db_session
    id_to_search = 1
    with pytest.raises(SortMapValueNotValidException):
        crud.update_sortmap(return_sortmap_schema, id_to_search, db)


def test_update_sortmap_wrong_id(test_db_session, return_sortmap_schema):
    db = test_db_session
    return_sortmap_schema.value = "01"
    id_to_search = 1000
    with pytest.raises(SortMapNotFoundException):
        crud.update_sortmap(return_sortmap_schema, id_to_search, db)


def test_delete_sortmap(test_db_session):
    db = test_db_session
    id_to_search = 1
    assert crud.delete_sortmap(id_to_search, db) == None


def test_delete_sortmap_wrong_id(test_db_session, return_sortmap_schema):
    db = test_db_session
    id_to_search = 100
    with pytest.raises(SortMapNotFoundException):
        crud.delete_sortmap(id_to_search, db)


def test_encrypt_message(
    test_db_session, return_message_to_encrypt, return_sortmap_correct_model
):
    db = test_db_session
    db.add(return_sortmap_correct_model)
    db.commit()
    response = crud.encrypt_message(
        return_message_to_encrypt.request, return_sortmap_correct_model.id, db
    )
    assert response == "98765543210"


def test_encrypt_message_wrong_id(
    test_db_session, return_message_to_encrypt, return_sortmap_correct_model
):
    db = test_db_session
    fake_id = 300
    with pytest.raises(SortMapNotFoundException):
        crud.encrypt_message(return_message_to_encrypt.request, fake_id, db)
