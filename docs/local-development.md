# Local Development

## Required Environment Variables

Use `.env` (copy from `.env.example`):

- `FIRESTORE_PROJECT_ID`
- `JWT_SECRET`
- `JWT_EXPIRATION_MINUTES`

## Main Local Commands

From repo root:

- `make up` -> starts API + Firestore emulator
- `make health` -> checks API readiness
- `make logs` -> API logs
- `make emulator-logs` -> emulator logs
- `make ps` -> running containers
- `make down` -> stop local stack

## Local Runtime Behavior

- API port: `8000`
- Emulator port: `8080`
- API uses `FIRESTORE_EMULATOR_HOST` in local mode.

## Demo for Non-Technical Stakeholders

Notebook demos are in `tests/`:

- `demo_happy_path.ipynb`
- `demo_error_scenarios.ipynb`

Suggested sequence:

1. `make up`
2. Open notebook in Jupyter
3. Run all cells top-to-bottom

## Common Local Flow (CLI)

1. Register user
2. Login and get token
3. Create product
4. Place order with token
5. List orders with token
