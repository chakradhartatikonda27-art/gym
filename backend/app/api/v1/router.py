from fastapi import APIRouter
from app.api.v1.endpoints import auth, members, attendance, shifts

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(members.router, prefix="/members", tags=["Member Onboarding & CRM"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["Smart Attendance"])
api_router.include_router(shifts.router, prefix="/shifts", tags=["Cash Register & Shifts"])
