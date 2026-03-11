# API Contract

Base URL (local): `http://localhost:8000`

## Health

- `GET /health`
- `200` -> `{"status":"ok"}`

## Auth

### Register

- `POST /auth/register`
- Body: `{"email":"...","password":"..."}`
- `201` -> `{"message":"user created"}`
- `409` -> `{"detail":"user already exists"}`

### Login

- `POST /auth/login`
- Body: `{"email":"...","password":"..."}`
- `200` -> `{"access_token":"...","token_type":"bearer","expires_in":3600}`
- `401` -> `{"detail":"no valid credentials"}`

## Products

### Create product

- `POST /products`
- Body: `{"product_id":"..." (optional),"product_name":"...","quantity":<int>=0}`
- `201` -> product object

### List products

- `GET /products`
- `200` -> list of product objects

### Get product

- `GET /products/{product_id}`
- `200` -> product object
- `404` -> `{"detail":"product not found"}`

### Update product

- `PUT /products/{product_id}`
- Body: `{"product_name":"...","quantity":<int>=0}`
- `200` -> updated product object
- `404` -> `{"detail":"product not found"}`

### Delete product

- `DELETE /products/{product_id}`
- `200` -> `{"message":"product deleted"}`
- `404` -> `{"detail":"product not found"}`

## Orders (JWT required)

Pass header: `Authorization: Bearer <access_token>`

### Place order

- `POST /orders`
- Body: `{"product_id":"...","quantity":<int>>0}`
- `201` -> `{"message":"order_placed","order":{...}}`
- `401` -> `{"detail":"no valid credentials"}`
- `404` -> `{"detail":"product not found"}`
- `409` -> `{"detail":"no_stock"}`
- `422` -> validation error payload

### List orders (current user)

- `GET /orders`
- `200` -> list of order objects
- `401` -> `{"detail":"no valid credentials"}`

### Get order by ID (current user)

- `GET /orders/{order_id}`
- `200` -> order object
- `401` -> `{"detail":"no valid credentials"}`
- `403` -> `{"detail":"forbidden"}`
- `404` -> `{"detail":"order not found"}`
