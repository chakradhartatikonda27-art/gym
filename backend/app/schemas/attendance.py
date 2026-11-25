from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class DynamicQRResponse(BaseModel):
    branch_id: str
    token: str
    expires_in_seconds: int = 15

class QRCheckinRequest(BaseModel):
    member_id: str
    qr_token: str

class QRCheckinResponse(BaseModel):
    decision: str             # ALLOWED, DENIED_EXPIRED, DENIED_FROZEN, DENIED_DUES_EXCEEDED
    rejection_reason: Optional[str] = None
    member_name: str
    days_remaining: int
    outstanding_dues: Decimal
