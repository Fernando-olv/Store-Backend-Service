from fastapi import FastAPI

app = FastAPI(title="Store Backend Service")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
