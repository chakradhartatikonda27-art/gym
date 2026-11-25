from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import uuid
from decimal import Decimal

from app.api.deps import get_db_with_tenant, get_current_user_payload
from app.schemas.auth import TokenPayload
from app.schemas.shift import ShiftOpenRequest, ShiftCloseRequest, ShiftResponse

router = APIRouter()

@router.post("/open", response_model=ShiftResponse)
async def open_shift(
    payload: ShiftOpenRequest,
    db: AsyncSession = Depends(get_db_with_tenant),
    user: TokenPayload = Depends(get_current_user_payload)
):
    shift_id = str(uuid.uuid4())
    insert_stmt = text("""
        INSERT INTO cash_registers (
            id, tenant_id, branch_id, opened_by_user_id, shift_name, opening_balance, shift_status
        ) VALUES (
            :id, :tenant_id, :branch_id, :user_id, :shift_name, :opening, 'OPEN'
        )
    """)
    await db.execute(insert_stmt, {
        "id": shift_id, "tenant_id": user.tenant_id, "branch_id": user.branch_id,
        "user_id": user.sub, "shift_name": payload.shift_name, "opening": payload.opening_balance
    })
    await db.commit()

    return ShiftResponse(
        shift_id=shift_id,
        shift_name=payload.shift_name,
        shift_status="OPEN",
        opening_balance=payload.opening_balance
    )

@router.post("/{shift_id}/close", response_model=ShiftResponse)
async def close_shift(
    shift_id: str,
    payload: ShiftCloseRequest,
    db: AsyncSession = Depends(get_db_with_tenant),
    user: TokenPayload = Depends(get_current_user_payload)
):
    # Fetch shift details
    shift_query = text("""
        SELECT id, shift_name, opening_balance, shift_status
        FROM cash_registers
        WHERE id = :shift_id AND tenant_id = :tenant_id
    """)
    res = await db.execute(shift_query, {"shift_id": shift_id, "tenant_id": user.tenant_id})
    shift = res.fetchone()
    if not shift or shift.shift_status != "OPEN":
        raise HTTPException(status_code=400, detail="Active open shift not found")

    # Calculate Cash Collected in this shift
    cash_query = text("""
        SELECT COALESCE(SUM(amount), 0.00) FROM payments
        WHERE cash_register_id = :shift_id AND payment_mode = 'CASH'
    """)
    cash_collected = (await db.execute(cash_query, {"shift_id": shift_id})).scalar()

    # Calculate Petty Cash Expenses
    exp_query = text("""
        SELECT COALESCE(SUM(amount), 0.00) FROM expenses
        WHERE cash_register_id = :shift_id AND payment_mode = 'CASH'
    """)
    expenses = (await db.execute(exp_query, {"shift_id": shift_id})).scalar()

    expected_cash = Decimal(str(shift.opening_balance)) + Decimal(str(cash_collected)) - Decimal(str(expenses))
    discrepancy = payload.counted_cash - expected_cash
    new_status = "DISCREPANCY_FLAGGED" if discrepancy != 0 else "CLOSED"

    update_stmt = text("""
        UPDATE cash_registers
        SET 
            closed_by_user_id = :user_id,
            closing_cash_counted = :counted,
            expected_cash_calculated = :expected,
            discrepancy_amount = :discrepancy,
            discrepancy_note = :note,
            shift_status = :status,
            closed_at = NOW()
        WHERE id = :shift_id
    """)
    await db.execute(update_stmt, {
        "user_id": user.sub, "counted": payload.counted_cash,
        "expected": expected_cash, "discrepancy": discrepancy,
        "note": payload.shortage_justification or payload.closing_notes,
        "status": new_status, "shift_id": shift_id
    })
    await db.commit()

    return ShiftResponse(
        shift_id=shift_id,
        shift_name=shift.shift_name,
        shift_status=new_status,
        opening_balance=shift.opening_balance,
        closing_cash_counted=payload.counted_cash,
        expected_cash_calculated=expected_cash,
        discrepancy_amount=discrepancy
    )
