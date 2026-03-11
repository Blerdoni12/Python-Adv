import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import analytics, auth, plans, recommendations, resources, sessions
from app.database.migrations import init_db
from app.utils.config import Settings
from app.utils.errors import AppError
from app.utils.logging import setup_logging

settings = Settings()
setup_logging(settings.log_level)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.exception_handler(AppError)
def handle_app_error(_, exc: AppError):
    logging.getLogger("app").warning("App error: %s", exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "errors": exc.details},
    )


app.include_router(auth.router, tags=["Auth"])
app.include_router(plans.router, prefix="/plans", tags=["Plans"])
app.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(resources.router, prefix="/resources", tags=["Resources"])
