from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID, uuid4
from sqlalchemy import (
    String, Text, Boolean, Integer, Numeric, Date, DateTime, 
    ForeignKey, UniqueConstraint, Index, text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.models.base import Base, TimestampMixin

class Tenant(Base, TimestampMixin):
    __tablename__ = "tenants"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    business_name: Mapped[str] = mapped_column(String(150), nullable=False)
    subdomain: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    contact_email: Mapped[str] = mapped_column(String(150), nullable=False)
    contact_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    tier: Mapped[str] = mapped_column(String(20), default="STARTER", nullable=False)
    whatsapp_monthly_quota: Mapped[int] = mapped_column(Integer, default=500, nullable=False)
    whatsapp_used_quota: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    branches: Mapped[List["Branch"]] = relationship("Branch", back_populates="tenant", cascade="all, delete-orphan")


class Branch(Base, TimestampMixin):
    __tablename__ = "branches"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    branch_name: Mapped[str] = mapped_column(String(100), nullable=False)
    branch_code: Mapped[str] = mapped_column(String(10), nullable=False)
    address_line: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    pincode: Mapped[str] = mapped_column(String(10), nullable=False)
    gstin: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    max_capacity: Mapped[int] = mapped_column(Integer, default=150, nullable=False)
    allow_grace_period_days: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    max_allowed_dues_threshold: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("500.00"), nullable=False)

    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="branches")

    __table_args__ = (
        UniqueConstraint("tenant_id", "branch_code", name="uq_tenant_branch_code"),
    )


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    branch_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("branches.id", ondelete="SET NULL"), nullable=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(30), default="RECEPTIONIST", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("tenant_id", "email", name="uq_tenant_user_email"),
        UniqueConstraint("tenant_id", "phone", name="uq_tenant_user_phone"),
    )


class Member(Base, TimestampMixin):
    __tablename__ = "members"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    home_branch_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    member_code: Mapped[str] = mapped_column(String(30), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    profile_photo_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    emergency_contact_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    emergency_contact_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    has_medical_conditions: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    medical_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    waiver_signed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    waiver_signed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("NOW()"), nullable=False)
    current_status: Mapped[str] = mapped_column(String(20), default="ACTIVE", nullable=False)
    last_attended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("tenant_id", "member_code", name="uq_tenant_member_code"),
        UniqueConstraint("tenant_id", "phone", name="uq_tenant_member_phone"),
        Index("idx_members_tenant_phone", "tenant_id", "phone"),
    )


class MembershipPlan(Base, TimestampMixin):
    __tablename__ = "membership_plans"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    plan_name: Mapped[str] = mapped_column(String(100), nullable=False)
    interval_unit: Mapped[str] = mapped_column(String(10), default="MONTHS", nullable=False)
    interval_value: Mapped[int] = mapped_column(Integer, nullable=False)
    base_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    joining_fee: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    tax_percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("18.00"), nullable=False)
    max_freeze_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class MemberSubscription(Base, TimestampMixin):
    __tablename__ = "member_subscriptions"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    branch_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    member_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    plan_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("membership_plans.id"), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    original_end_date: Mapped[date] = mapped_column(Date, nullable=False)
    current_end_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_frozen_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE", nullable=False)

    __table_args__ = (
        Index("idx_subscriptions_tenant_member", "tenant_id", "member_id", "status"),
    )


class Invoice(Base, TimestampMixin):
    __tablename__ = "invoices"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    branch_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    member_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    subscription_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("member_subscriptions.id"), nullable=True)
    invoice_number: Mapped[str] = mapped_column(String(50), nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    paid_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    balance_due: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="UNPAID", nullable=False)
    issued_by_user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("tenant_id", "invoice_number", name="uq_tenant_invoice_number"),
        Index("idx_invoices_tenant_member_dues", "tenant_id", "member_id", "balance_due"),
    )


class CashRegister(Base):
    __tablename__ = "cash_registers"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    branch_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    opened_by_user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    closed_by_user_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    shift_name: Mapped[str] = mapped_column(String(50), default="MORNING", nullable=False)
    opening_balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    closing_cash_counted: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    expected_cash_calculated: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    discrepancy_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    discrepancy_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    shift_status: Mapped[str] = mapped_column(String(20), default="OPEN", nullable=False)
    opened_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("NOW()"), nullable=False)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    branch_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    invoice_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    cash_register_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("cash_registers.id"), nullable=True)
    payment_mode: Mapped[str] = mapped_column(String(20), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    reference_transaction_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="SUCCESS", nullable=False)
    collected_by_user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("NOW()"), nullable=False)


class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    branch_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    member_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    checkin_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("NOW()"), nullable=False)
    checkout_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    method: Mapped[str] = mapped_column(String(20), default="DYNAMIC_QR", nullable=False)
    decision: Mapped[str] = mapped_column(String(30), default="ALLOWED", nullable=False)
    rejection_reason: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    verified_by_user_id: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    device_identifier: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
