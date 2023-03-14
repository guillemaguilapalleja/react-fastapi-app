from typing import Any
from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.database import Base
from backend.models import SortMaps
from backend.schemas import SortMapSchema, RequestSchema


@pytest.fixture(scope="session")
def test_db_session():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    session = Session(bind=connection)
    yield session
    session.close()
    connection.close()
    engine.dispose()


@pytest.fixture
def return_sortmap():
    return SortMaps(value="Test")


@pytest.fixture
def return_sortmap_schema():
    return SortMapSchema(value="Test")


@pytest.fixture
def return_correct_sortmap_schema():
    return SortMapSchema(value="01")


@pytest.fixture
def return_sortmap_correct_model():
    return SortMaps(value="9876543210", id=200)


@pytest.fixture
def return_message_to_encrypt():
    return RequestSchema(request="12345567890")
