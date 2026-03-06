from fastapi import FastAPI

from app.routers import auth, orders, products

app = FastAPI(title="Store Backend Service")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
