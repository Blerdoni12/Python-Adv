from fastapi import FastAPI
from routers import study_plan, api_key
from database import create_database

app = FastAPI(title="Study Planner API")

app.include_router(study_plan.router, prefix="/plans", tags=["Study Plans"])
app.include_router(api_key.router, prefix="/validate_key", tags=["Auth"])


@app.on_event("startup")
def startup():
    create_database()