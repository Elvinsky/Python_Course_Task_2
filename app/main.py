"""Application entry point: `uv run uvicorn app.main:app --reload`, then open http://127.0.0.1:8000/docs."""

from fastapi import FastAPI

from app.routers import items

app = FastAPI(
    title="Inventory API",
    version="0.1.0",
    description="Product inventory catalog (Python Kick-Start, Task 2).",
)
app.include_router(items.router)
