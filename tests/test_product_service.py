from app.services.product_service import derive_status


def test_derive_status_in_stock() -> None:
    assert derive_status(5) == "in_stock"


def test_derive_status_out_of_stock() -> None:
    assert derive_status(0) == "out_of_stock"
