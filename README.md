# Store Backend Service

Store Backend Service is a backend project for a store platform.

The infrastructure is managed with Terraform on Google Cloud, while the API is built with FastAPI and Firestore.

## Tech Stack

- Python (FastAPI)
- Firestore (Emulator locally, managed Firestore in GCP)
- Terraform
- Google Cloud Platform (GCP)
- Docker

## Local Development (Docker)

### Prerequisites

- Docker installed and running
- Your user has access to Docker daemon (`docker` group)

### Environment

Create `.env` from `.env.example` and set at least:

- `FIRESTORE_PROJECT_ID`
- `JWT_SECRET`
- `JWT_EXPIRATION_MINUTES`

### Quickstart

```bash
make up
make health
```

Expected response:

```json
{"status":"ok"}
```

Useful commands:

```bash
make logs
make emulator-logs
make ps
make down
```

### Production-like local run (no reload mount)

```bash
make prod
make health
make prod-down
```

## API Overview

### Auth

- `POST /auth/register`
- `POST /auth/login`

### Products

- `POST /products`
- `GET /products`
- `GET /products/{product_id}`
- `PUT /products/{product_id}`
- `DELETE /products/{product_id}`

### Orders (JWT required)

- `POST /orders`
- `GET /orders`
- `GET /orders/{order_id}`

## Common Local Flow

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"buyer@example.com","password":"strongpass123"}'

# Login
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"buyer@example.com","password":"strongpass123"}' | jq -r '.access_token')

# Seed product
make seed-products

# Place order
curl -X POST http://localhost:8000/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id":"p001","quantity":1}'
```
