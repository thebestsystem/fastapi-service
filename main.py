"""FastAPI service — accessible from Hermes via the Railway private network.

Run: uvicorn main:app --host 0.0.0.0 --port 8000
All routes require the `x-api-key` header to match the API_KEY env var.
"""
import os

from fastapi import Depends, FastAPI, Header, HTTPException

API_KEY = os.environ.get("API_KEY", "").strip()
if not API_KEY:
    raise RuntimeError("API_KEY environment variable is not set")

app = FastAPI(title="FastAPI Service", version="1.0.0")


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing x-api-key")


@app.get("/", dependencies=[Depends(require_api_key)])
def root() -> dict:
    return {"service": "fastapi-service", "version": "1.0.0", "status": "ok"}


@app.get("/health", dependencies=[Depends(require_api_key)])
def health() -> dict:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
