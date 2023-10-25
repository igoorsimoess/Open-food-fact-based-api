import requests
from rest_framework import status

API = "http://127.0.0.1:8000"
VALID_PRODUCT_CODE = "7896004006642"
INVALID_PRODUCT_CODE = "000"


def test_info():
    """
    ensures get request returns 200
    """

    response = requests.get(API + "/info")

    assert response.status_code == status.HTTP_200_OK


def test_info_data():
    """
    ensures response contains expected fields
    """

    response = requests.get(API + "/info")
    expected_fields = [
        "db_connection",
        "last_cron_exec",
        "running_time",
        "memory_usage",
    ]

    # ensures response contains expected fields
    assert all(field in expected_fields for field in response.json())


def test_list_200_ok():
    """
    ensures get request's ok
    """

    response = requests.get(API + "/products")

    assert response.status_code == status.HTTP_200_OK


def test_list_pagination():
    """
    ensures get request's ok and response cpntains expected fields
    """

    response = requests.get(API + "/products")
    assert len(response.json()["results"]) == 10


def test_retrieve_200_ok():
    """
    ensures get request's ok and response cpntains expected fields
    """

    response = requests.get(f"{API}/products/{VALID_PRODUCT_CODE}")

    assert response.status_code == status.HTTP_200_OK


def test_retrieve_data():
    """
    ensures get request's ok and response cpntains expected fields
    """
    expected_fields = [
        "code",
        "status",
        "imported_t",
        "url",
        "creator",
        "created_t",
        "last_modified_t",
        "product_name",
        "quantity",
        "brands",
        "categories",
        "stores",
        "labels",
        "cities",
        "purchase_places",
        "ingredients_text",
        "traces",
        "serving_size",
        "serving_quantity",
        "nutriscore_score",
        "nutriscore_grade",
        "main_category",
        "image_url",
    ]

    response = requests.get(f"{API}/products/{VALID_PRODUCT_CODE}")
    assert all(field in expected_fields for field in response.json())


def test_retrieve_404():
    """
    ensures get request returns 404 is a product code is not valid
    """

    response = requests.get(f"{API}/products/{INVALID_PRODUCT_CODE}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_put_200_ok():
    """
    ensures get request's ok and response cpntains expected fields
    """
    to_update_data = {"code": VALID_PRODUCT_CODE, "traces": "teste_put"}

    response = requests.put(
        f"{API}/products/{VALID_PRODUCT_CODE}/", json=to_update_data
    )
    assert response.status_code == status.HTTP_200_OK


def test_put_data():
    """
    ensures get request's ok and response cpntains expected fields
    """

    to_update_data = {"code": VALID_PRODUCT_CODE, "traces": "teste_put"}

    response = requests.put(
        f"{API}/products/{VALID_PRODUCT_CODE}/", json=to_update_data
    )

    assert response.json()["traces"] == to_update_data["traces"]


def test_destroy_code():
    """
    ensures get request's ok and response cpntains expected fields
    """
    response = requests.delete(f"{API}/products/{VALID_PRODUCT_CODE}")

    assert response.status_code == status.HTTP_200_OK


def test_destroy_data():
    """
    ensures get request's ok and response cpntains expected fields
    """
    response = requests.delete(f"{API}/products/{VALID_PRODUCT_CODE}")

    assert response.json()[0]["status"] == "trash"
