from unittest import mock
from fastapi import status
from fastapi.testclient import TestClient

from backend.exceptions import (
    SortMapValueNotValidException,
    SortMapNotFoundException,
    MessageToEncryptNotValidException,
)
from backend.main import app
from backend.models import SortMaps
from backend.schemas import SortMapSchema, RequestSchema

client = TestClient(app)


@mock.patch("backend.crud.create_sortmap")
def test_create_sortmap(mock_sortmap):
    value = "01"
    mock_sortmap.return_value = SortMaps(id=1, value=value)
    response = client.post("/api/sortmap", json={"value": value})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] == 1
    assert data["value"] == value


@mock.patch("backend.crud.create_sortmap")
def test_create_sortmap_no_digit(mock_error):
    value = "Hello"
    response = client.post("/api/sortmap", json={"value": value})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert data["detail"] == "A SortMap must be a string of digits only (0123456789)"


@mock.patch("backend.crud.create_sortmap", side_effect=SortMapValueNotValidException)
def test_create_sortmap_duplicated_numbers(mock_error):
    value = "11"
    response = client.post("/api/sortmap", json={"value": value})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert data["detail"] == "A SortMap can not have duplicates numbers in it"


@mock.patch("backend.crud.get_sortmap_by_id")
def test_get_sortmap_by_id(get_mock_sortmap):
    mock_sortmap = SortMaps(id=1, value="Test")
    get_mock_sortmap.return_value = mock_sortmap
    response = client.get("/api/sortmaps", params={"sortmap_id": mock_sortmap.id})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["value"] == "Test"


@mock.patch("backend.crud.get_sortmap_by_id", side_effect=SortMapNotFoundException)
def test_get_sortmap_by_wrong_id(get_mock_sortmap):
    mock_id = "1"
    response = client.get("/api/sortmaps", params={"sortmap_id": mock_id})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == f"There is no SortMap with id={mock_id}"


@mock.patch("backend.crud.get_sortmaps_list")
def test_get_sortmaps_empty_list(get_mock_sortmaps_list):
    response = client.get("/api/sortmaps_list")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 0


@mock.patch("backend.crud.get_sortmaps_list")
def test_get_sortmaps_list(get_mock_sortmaps_list):
    mock_id = "1"
    mock_value = "01"
    get_mock_sortmaps_list.return_value = [{"id": mock_id, "value": mock_value}]
    response = client.get("/api/sortmaps_list")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == mock_id
    assert data[0]["value"] == mock_value


@mock.patch("backend.crud.update_sortmap")
def test_update_sortmap(mock_update_sortmap):
    mock_id = 1
    mock_value = "01"
    mock_value_to_update = SortMapSchema(value="1")
    mock_update_sortmap.return_value = {"id": mock_id, "value": mock_value}
    response = client.put(f"/api/sortmap/{mock_id}", json=mock_value_to_update.dict())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == mock_id
    assert data["value"] == "01"


@mock.patch("backend.crud.update_sortmap", side_effect=SortMapNotFoundException)
def test_update_sortmap_bad_id(mock_update_sortmap):
    mock_id = 1
    mock_value_to_update = SortMapSchema(value="1")
    response = client.put(f"/api/sortmap/{mock_id}", json=mock_value_to_update.dict())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == f"There is no SortMap with id={mock_id}"


@mock.patch("backend.crud.update_sortmap", side_effect=SortMapValueNotValidException)
def test_update_sortmap_value_not_valid(mock_update_sortmap):
    mock_id = 1
    mock_value_to_update = SortMapSchema(value="1")
    response = client.put(f"/api/sortmap/{mock_id}", json=mock_value_to_update.dict())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert (
        data["detail"]
        == "A SortMap must be a string of digits only (0123456789) and can not have duplicates in it"
    )


@mock.patch("backend.crud.get_sortmap_by_id")
@mock.patch("backend.crud.delete_sortmap")
def test_delete_sortmap(mock_deleted_sortmap, mock_sortmap):
    mock_id = 1
    mock_value = "1"
    mock_sortmap.return_value = SortMaps(id=mock_id, value=mock_value)
    mock_deleted_sortmap.return_value = None
    response = client.delete(f"/api/sortmap/{mock_id}")
    assert response.status_code == status.HTTP_200_OK


@mock.patch("backend.crud.get_sortmap_by_id", side_effect=SortMapNotFoundException)
def test_delete_sortmap_bad_id(mock_sortmap):
    mock_id = 1
    response = client.delete(f"/api/sortmap/{mock_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == f"There is no SortMap with id={mock_id}"


@mock.patch("backend.crud.encrypt_message")
def test_encrypt_message(mock_sortmap):
    mock_id = 1
    message_to_encrypt = "12345567890"
    mock_sortmap.return_value = "98765543210"
    mock_request = RequestSchema(request=message_to_encrypt)
    response = client.post(f"/api/order?sortmap_id={mock_id}", json=mock_request.dict())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["sortmap_id"] == 1
    assert data["response"] == "98765543210"
    assert isinstance(data["time"], float)


@mock.patch(
    "backend.crud.encrypt_message", side_effect=MessageToEncryptNotValidException
)
def test_encrypt_bad_message(mock_sortmap):
    mock_id = 1
    response = client.post(f"/api/order?sortmap_id={mock_id}", json={"request": "01"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert (
        data["detail"]
        == "A SortMap must be a string of digits only (0123456789) and can not have duplicates in it"
    )


@mock.patch("backend.crud.encrypt_message", side_effect=SortMapNotFoundException)
def test_encrypt_message_bad_sortmap_id(mock_sortmap):
    mock_id = 1
    response = client.post(f"/api/order?sortmap_id={mock_id}", json={"request": "01"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == f"There is no SortMap with id={mock_id}"
