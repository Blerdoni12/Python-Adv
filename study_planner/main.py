from fastapi import FastAPI
from routers import plans, users
from database import create_database

app = FastAPI(title="Study Planner API")

app.include_router(plans.router, prefix="/api/plans", tags=["Plans"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])

@app.on_event("startup")
def startup():
    create_database()