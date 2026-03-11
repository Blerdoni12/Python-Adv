from fastapi import APIRouter, Depends

from app.auth.deps import get_current_user
from app.schemas.plan import PlanCreate, PlanPublic, PlanUpdate
from app.services import plans as plan_service

router = APIRouter()


@router.get("/", response_model=list[PlanPublic])
def list_plans(current_user: dict = Depends(get_current_user)):
    return plan_service.get_plans_for_user(current_user["id"])


@router.post("/", response_model=PlanPublic)
def create_plan(payload: PlanCreate, current_user: dict = Depends(get_current_user)):
    return plan_service.create_plan(
        current_user["id"],
        payload.subject,
        payload.deadline,
        payload.priority.value,
        payload.estimated_hours,
        payload.status.value,
    )


@router.put("/{plan_id}", response_model=PlanPublic)
def update_plan(plan_id: int, payload: PlanUpdate, current_user: dict = Depends(get_current_user)):
    return plan_service.update_plan(
        current_user["id"],
        plan_id,
        payload.subject,
        payload.deadline,
        payload.priority.value,
        payload.estimated_hours,
        payload.status.value,
    )


@router.delete("/{plan_id}")
def delete_plan(plan_id: int, current_user: dict = Depends(get_current_user)):
    plan_service.delete_plan(current_user["id"], plan_id)
    return {"message": "Plan deleted"}
