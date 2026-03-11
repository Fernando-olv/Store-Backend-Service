# Testing and Quality

## Test Commands

- `make test` -> runs `pytest`
- `pytest -q` -> direct test run

## Static Quality Commands

- `make lint` -> `ruff check .`
- `make format` -> `ruff format .`

## Useful Targeted Tests

- `pytest -q tests/test_jwt_service.py`
- `pytest -q tests/test_product_service.py`

## Known Pitfalls

1. `No module named app`
- Ensure tests run from repo root.
- `pytest.ini` includes `pythonpath = .`.

2. Python version mismatch
- Code supports Python 3.10+.
- Uses `timezone.utc` (not `datetime.UTC`) for compatibility.

3. Missing dependencies locally
- If imports fail (`jose`, etc.), run `pip install -r requirements.txt` in active env.

4. Root-owned cache artifacts
- Old `__pycache__` can cause permission noise in some commands.
- Prefer non-root local Python runs.
