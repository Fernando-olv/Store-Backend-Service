import json
import os
import time
import uuid
import urllib.error
import urllib.request
from typing import Any

BASE_URL = os.getenv("INTEGRATION_BASE_URL", "http://localhost:8000").rstrip("/")
REQUEST_TIMEOUT_SECONDS = 20


def _request_json(
    method: str,
    path: str,
    expected_status: int,
    payload: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> Any:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request_headers: dict[str, str] = {"Accept": "application/json"}
    if payload is not None:
        request_headers["Content-Type"] = "application/json"
    if headers:
        request_headers.update(headers)

    request = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=body,
        headers=request_headers,
        method=method,
    )

    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            status_code = response.status
            response_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        status_code = exc.code
        response_body = exc.read().decode("utf-8")

    assert status_code == expected_status, response_body
    return json.loads(response_body) if response_body else None


def test_auth_product_order_flow() -> None:
    suffix = uuid.uuid4().hex[:8]
    email = f"ci-user-{suffix}@example.com"
    password = "strongpass123"
    product_id = f"ci-product-{suffix}"

    register_response = _request_json(
        method="POST",
        path="/auth/register",
        expected_status=201,
        payload={"email": email, "password": password},
    )
    assert register_response == {"message": "user created"}

    login_response = _request_json(
        method="POST",
        path="/auth/login",
        expected_status=200,
        payload={"email": email, "password": password},
    )
    token = login_response["access_token"]
    assert login_response["token_type"] == "bearer"
    assert login_response["expires_in"] == 3600

    create_product_response = _request_json(
        method="POST",
        path="/products",
        expected_status=201,
        payload={
            "product_id": product_id,
            "product_name": "CI Product",
            "quantity": 2,
        },
    )
    assert create_product_response["product_id"] == product_id
    assert create_product_response["status"] == "in_stock"
    assert create_product_response["quantity"] == 2

    auth_headers = {"Authorization": f"Bearer {token}"}
    place_order_response = _request_json(
        method="POST",
        path="/orders",
        expected_status=201,
        payload={"product_id": product_id, "quantity": 1},
        headers=auth_headers,
    )
    assert place_order_response["message"] == "order_placed"
    order_id = place_order_response["order"]["order_id"]
    assert place_order_response["order"]["buyer_email"] == email
    assert place_order_response["order"]["product_id"] == product_id
    assert place_order_response["order"]["quantity"] == 1

    for _ in range(3):
        list_orders_response = _request_json(
            method="GET",
            path="/orders",
            expected_status=200,
            headers=auth_headers,
        )
        if any(order["order_id"] == order_id for order in list_orders_response):
            break
        time.sleep(1)
    else:
        raise AssertionError(f"Order {order_id} not returned by GET /orders")
