"""Minimal demo service. Test supply-chain controls, not a production application."""
import os

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI(title="DevSecOps Demo", docs_url=None, redoc_url=None)

class BasicHeaders(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Frame-Options"] = "DENY"
        return response

app.add_middleware(BasicHeaders)

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.get("/v1/build")
def build_information():
    # Never return environment variables or internal configuration wholesale.
    return {"service": "devsecops-demo", "revision": os.getenv("APP_REVISION", "local")}
