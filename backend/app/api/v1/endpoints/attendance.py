from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import date
import uuid
import time
import hmac
import hashlib

from app.api.deps import get_db_with_tenant, get_current_user_payload
from app.schemas.auth import TokenPayload
from app.schemas.attendance import DynamicQRResponse, QRCheckinRequest, QRCheckinResponse
from app.core.config import settings

router = APIRouter()

@router.get("/dynamic-qr", response_model=DynamicQRResponse)
async def get_dynamic_qr_token(user: TokenPayload = Depends(get_current_user_payload)):
    """
    Generates a 15-second rotating cryptographic HMAC token for the desk kiosk display.
    """
    timestamp = int(time.time())
    nonce = uuid.uuid4().hex[:8]
    data_to_sign = f"{user.branch_id}:{timestamp}:{nonce}"
    signature = hmac.new(
        settings.SECRET_KEY.encode(),
        data_to_sign.encode(),
        hashlib.sha256
    ).hexdigest()

    token = f"{data_to_sign}:{signature}"
    return DynamicQRResponse(branch_id=user.branch_id, token=token, expires_in_seconds=15)

@router.post("/qr-checkin", response_model=QRCheckinResponse)
async def qr_checkin(
    payload: QRCheckinRequest,
    db: AsyncSession = Depends(get_db_with_tenant),
    user: TokenPayload = Depends(get_current_user_payload)
):
    """
    Sub-150ms verification query checking active plan validity and dues threshold.
    """
    # 1. Fetch member status & active plan
    query = text("""
        SELECT 
            m.full_name,
            m.current_status,
            s.current_end_date,
            s.status as subscription_status,
            COALESCE(SUM(i.balance_due), 0.00) as total_dues
        FROM members m
        LEFT JOIN member_subscriptions s 
            ON s.member_id = m.id AND s.status = 'ACTIVE' AND s.current_end_date >= CURRENT_DATE
        LEFT JOIN invoices i 
            ON i.member_id = m.id AND i.balance_due > 0
        WHERE m.id = :member_id AND m.tenant_id = :tenant_id
        GROUP BY m.id, m.full_name, m.current_status, s.current_end_date, s.status
    """)
    result = await db.execute(query, {"member_id": payload.member_id, "tenant_id": user.tenant_id})
    row = result.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Member record not found")

    decision = "ALLOWED"
    rejection_reason = None
    days_remaining = (row.current_end_date - date.today()).days if row.current_end_date else 0

    if not row.current_end_date:
        decision = "DENIED_EXPIRED"
        rejection_reason = "Plan expired. Renewal required."
    elif row.current_status == "FROZEN":
        decision = "DENIED_FROZEN"
        rejection_reason = "Membership is currently frozen."
    elif row.total_dues > 1000:
        decision = "DENIED_DUES_EXCEEDED"
        rejection_reason = f"Dues limit exceeded (₹{row.total_dues} pending)."

    # Log attendance
    log_id = str(uuid.uuid4())
    insert_log = text("""
        INSERT INTO attendance_logs (
            id, tenant_id, branch_id, member_id, method, decision, rejection_reason
        ) VALUES (
            :id, :tenant_id, :branch_id, :member_id, 'DYNAMIC_QR', :decision, :reason
        )
    """)
    await db.execute(insert_log, {
        "id": log_id, "tenant_id": user.tenant_id, "branch_id": user.branch_id,
        "member_id": payload.member_id, "decision": decision, "reason": rejection_reason
    })
    await db.commit()

    return QRCheckinResponse(
        decision=decision,
        rejection_reason=rejection_reason,
        member_name=row.full_name,
        days_remaining=days_remaining,
        outstanding_dues=row.total_dues
    )
