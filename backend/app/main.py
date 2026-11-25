from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

from app.routers import (
    accounts,
    ai,
    auth,
    budgets,
    categories,
    forecast,
    imports,
    planning,
    reports,
    transactions,
)

app = FastAPI(title="FinanceSEME API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

for module in (
    auth,
    accounts,
    categories,
    transactions,
    budgets,
    planning,
    reports,
    forecast,
    imports,
    ai,
):
    app.include_router(module.router)


@app.get("/health")
def health():
    return {"status": "ok"}
