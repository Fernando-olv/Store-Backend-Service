# Backend Architecture

## Layered Structure

The FastAPI app follows this path:

`router -> service -> repository -> Firestore`

### Routers (`app/routers`)

- Define HTTP endpoints and status mappings.
- Translate service exceptions into API responses.

### Services (`app/services`)

- Hold business logic.
- Manage auth, token handling, and order orchestration.
- `order_service` enforces transactional stock updates.

### Repositories (`app/repositories`)

- Encapsulate Firestore collection access.
- Avoid HTTP concerns and business branching.

### Models (`app/models`)

- Pydantic request/response contracts.
- Input validation constraints (e.g., quantity bounds).

## Firestore Integration

- Firestore client created in `firestore_client.py`.
- Project ID sourced from `FIRESTORE_PROJECT_ID` or `GOOGLE_CLOUD_PROJECT`.
- Local mode uses emulator via `FIRESTORE_EMULATOR_HOST` env variable.

## Auth Flow

1. Register user (`/auth/register`) with hashed password.
2. Login (`/auth/login`) and receive JWT.
3. Protected routes extract and validate `Authorization: Bearer <token>`.
4. Subject (`sub`) claim is buyer identity (`buyer_email`).

## Order Placement Flow

1. Validate JWT and payload.
2. Start Firestore transaction.
3. Read product stock.
4. Reject with `no_stock` if insufficient quantity.
5. Decrement stock and recompute product status.
6. Create order document atomically.
