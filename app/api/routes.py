from fastapi import APIRouter
from app.api.endpoints import users, items, payroll

router = APIRouter()

# Include endpoint routers
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(items.router, prefix="/items", tags=["items"])
router.include_router(payroll.router, prefix="/payroll", tags=["payroll"])
