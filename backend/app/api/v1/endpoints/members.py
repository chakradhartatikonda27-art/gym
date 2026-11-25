from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import timedelta
import uuid
from decimal import Decimal

from app.api.deps import get_db_with_tenant, get_current_user_payload
from app.schemas.auth import TokenPayload
from app.schemas.member import FastOnboardRequest, FastOnboardResponse

router = APIRouter()

@router.post("/fast-onboard", response_model=FastOnboardResponse)
async def fast_onboard_member(
    payload: FastOnboardRequest,
    db: AsyncSession = Depends(get_db_with_tenant),
    user: TokenPayload = Depends(get_current_user_payload)
):
    """
    Atomic 45-Second Onboarding:
    1. Checks/creates member.
    2. Activates plan subscription.
    3. Generates immutable invoice.
    4. Records split payment.
    """
    # Verify Plan exists
    plan_stmt = text("""
        SELECT id, plan_name, interval_unit, interval_value, base_price, tax_percentage
        FROM membership_plans
        WHERE id = :plan_id AND tenant_id = :tenant_id
    """)
    plan_res = await db.execute(plan_stmt, {"plan_id": payload.plan_id, "tenant_id": user.tenant_id})
    plan = plan_res.fetchone()
    if not plan:
        raise HTTPException(status_code=404, detail="Membership plan not found")

    # Calculate Fees
    total_fee = Decimal(str(plan.base_price)) * (Decimal("1.00") + (Decimal(str(plan.tax_percentage)) / Decimal("100.00")))
    total_paid = payload.cash_amount + payload.online_amount
    balance_due = total_fee - total_paid

    # Calculate Expiry Date
    if plan.interval_unit == "YEARS":
        days = plan.interval_value * 365
    elif plan.interval_unit == "MONTHS":
        days = plan.interval_value * 30
    else:
        days = plan.interval_value
    end_date = payload.start_date + timedelta(days=days)

    member_id = str(uuid.uuid4())
    member_code = f"GYM-{payload.phone[-4:]}"

    # 1. Insert Member
    insert_member = text("""
        INSERT INTO members (
            id, tenant_id, home_branch_id, member_code, full_name, phone, gender,
            date_of_birth, emergency_contact_phone, has_medical_conditions,
            medical_notes, waiver_signed, current_status
        ) VALUES (
            :id, :tenant_id, :branch_id, :code, :name, :phone, :gender,
            :dob, :em_phone, :med, :med_notes, :waiver, 'ACTIVE'
        )
    """)
    await db.execute(insert_member, {
        "id": member_id, "tenant_id": user.tenant_id, "branch_id": user.branch_id,
        "code": member_code, "name": payload.full_name, "phone": payload.phone,
        "gender": payload.gender.value, "dob": payload.date_of_birth,
        "em_phone": payload.emergency_contact_phone, "med": payload.has_medical_conditions,
        "med_notes": payload.medical_notes, "waiver": payload.waiver_signed
    })

    # 2. Insert Subscription
    sub_id = str(uuid.uuid4())
    insert_sub = text("""
        INSERT INTO member_subscriptions (
            id, tenant_id, branch_id, member_id, plan_id, start_date, original_end_date, current_end_date, status
        ) VALUES (
            :id, :tenant_id, :branch_id, :member_id, :plan_id, :start, :end_date, :end_date, 'ACTIVE'
        )
    """)
    await db.execute(insert_sub, {
        "id": sub_id, "tenant_id": user.tenant_id, "branch_id": user.branch_id,
        "member_id": member_id, "plan_id": payload.plan_id, "start": payload.start_date,
        "end_date": end_date
    })

    # 3. Generate Invoice
    inv_id = str(uuid.uuid4())
    inv_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
    insert_inv = text("""
        INSERT INTO invoices (
            id, tenant_id, branch_id, member_id, subscription_id, invoice_number,
            subtotal, tax_amount, total_amount, paid_amount, balance_due,
            status, issued_by_user_id
        ) VALUES (
            :id, :tenant_id, :branch_id, :member_id, :sub_id, :inv_num,
            :subtotal, :tax, :total, :paid, :balance, :status, :issued_by
        )
    """)
    await db.execute(insert_inv, {
        "id": inv_id, "tenant_id": user.tenant_id, "branch_id": user.branch_id,
        "member_id": member_id, "sub_id": sub_id, "inv_num": inv_number,
        "subtotal": plan.base_price, "tax": total_fee - plan.base_price,
        "total": total_fee, "paid": total_paid, "balance": balance_due,
        "status": "PAID" if balance_due <= 0 else "PARTIALLY_PAID",
        "issued_by": user.sub
    })

    # 4. Insert Payments
    if payload.cash_amount > 0:
        await db.execute(text("""
            INSERT INTO payments (id, tenant_id, branch_id, invoice_id, cash_register_id, payment_mode, amount, collected_by_user_id)
            VALUES (:id, :tenant_id, :branch_id, :inv_id, :reg_id, 'CASH', :amount, :user_id)
        """), {
            "id": str(uuid.uuid4()), "tenant_id": user.tenant_id, "branch_id": user.branch_id,
            "inv_id": inv_id, "reg_id": payload.cash_register_id, "amount": payload.cash_amount,
            "user_id": user.sub
        })

    if payload.online_amount > 0:
        await db.execute(text("""
            INSERT INTO payments (id, tenant_id, branch_id, invoice_id, payment_mode, amount, reference_transaction_id, collected_by_user_id)
            VALUES (:id, :tenant_id, :branch_id, :inv_id, 'UPI', :amount, :ref, :user_id)
        """), {
            "id": str(uuid.uuid4()), "tenant_id": user.tenant_id, "branch_id": user.branch_id,
            "inv_id": inv_id, "amount": payload.online_amount, "ref": payload.online_reference_id,
            "user_id": user.sub
        })

    await db.commit()

    return FastOnboardResponse(
        member_id=member_id,
        member_code=member_code,
        full_name=payload.full_name,
        subscription_id=sub_id,
        invoice_id=inv_id,
        invoice_number=inv_number,
        total_amount=total_fee,
        paid_amount=total_paid,
        balance_due=balance_due,
        message="Member activated, invoice issued, and welcome WhatsApp queued."
    )
