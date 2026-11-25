"""Initial production schema and row-level security setup

Revision ID: 0001_initial
Revises: 
Create Date: 2026-11-22
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1. Enable Extensions
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')

    # 2. Tenants Table
    op.create_table(
        'tenants',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('business_name', sa.String(150), nullable=False),
        sa.Column('subdomain', sa.String(50), unique=True, nullable=False),
        sa.Column('contact_email', sa.String(150), nullable=False),
        sa.Column('contact_phone', sa.String(20), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('tier', sa.String(20), server_default='STARTER', nullable=False),
        sa.Column('whatsapp_monthly_quota', sa.Integer(), server_default='500', nullable=False),
        sa.Column('whatsapp_used_quota', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False)
    )

    # 3. Branches Table
    op.create_table(
        'branches',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('branch_name', sa.String(100), nullable=False),
        sa.Column('branch_code', sa.String(10), nullable=False),
        sa.Column('address_line', sa.Text(), nullable=False),
        sa.Column('city', sa.String(50), nullable=False),
        sa.Column('state', sa.String(50), nullable=False),
        sa.Column('pincode', sa.String(10), nullable=False),
        sa.Column('gstin', sa.String(20), nullable=True),
        sa.Column('max_capacity', sa.Integer(), server_default='150', nullable=False),
        sa.Column('allow_grace_period_days', sa.Integer(), server_default='2', nullable=False),
        sa.Column('max_allowed_dues_threshold', sa.Numeric(10, 2), server_default='500.00', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.UniqueConstraint('tenant_id', 'branch_code', name='uq_tenant_branch_code')
    )

    # 4. Users Table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('branch_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('branches.id', ondelete='SET NULL'), nullable=True),
        sa.Column('full_name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(150), nullable=False),
        sa.Column('phone', sa.String(20), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(30), server_default='RECEPTIONIST', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.UniqueConstraint('tenant_id', 'email', name='uq_tenant_user_email'),
        sa.UniqueConstraint('tenant_id', 'phone', name='uq_tenant_user_phone')
    )

    # 5. Members Table
    op.create_table(
        'members',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('home_branch_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('branches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('member_code', sa.String(30), nullable=False),
        sa.Column('full_name', sa.String(100), nullable=False),
        sa.Column('phone', sa.String(20), nullable=False),
        sa.Column('email', sa.String(150), nullable=True),
        sa.Column('gender', sa.String(10), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('profile_photo_url', sa.Text(), nullable=True),
        sa.Column('emergency_contact_name', sa.String(100), nullable=True),
        sa.Column('emergency_contact_phone', sa.String(20), nullable=True),
        sa.Column('has_medical_conditions', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('medical_notes', sa.Text(), nullable=True),
        sa.Column('waiver_signed', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('waiver_signed_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('current_status', sa.String(20), server_default='ACTIVE', nullable=False),
        sa.Column('last_attended_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.UniqueConstraint('tenant_id', 'member_code', name='uq_tenant_member_code'),
        sa.UniqueConstraint('tenant_id', 'phone', name='uq_tenant_member_phone')
    )

    # 6. Membership Plans Table
    op.create_table(
        'membership_plans',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('plan_name', sa.String(100), nullable=False),
        sa.Column('interval_unit', sa.String(10), server_default='MONTHS', nullable=False),
        sa.Column('interval_value', sa.Integer(), nullable=False),
        sa.Column('base_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('joining_fee', sa.Numeric(10, 2), server_default='0.00', nullable=False),
        sa.Column('tax_percentage', sa.Numeric(5, 2), server_default='18.00', nullable=False),
        sa.Column('max_freeze_days', sa.Integer(), server_default='0', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False)
    )

    # 7. Member Subscriptions Table
    op.create_table(
        'member_subscriptions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('branch_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('branches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('member_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('members.id', ondelete='CASCADE'), nullable=False),
        sa.Column('plan_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('membership_plans.id'), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('original_end_date', sa.Date(), nullable=False),
        sa.Column('current_end_date', sa.Date(), nullable=False),
        sa.Column('total_frozen_days', sa.Integer(), server_default='0', nullable=False),
        sa.Column('status', sa.String(20), server_default='ACTIVE', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False)
    )

    # 8. Invoices Table
    op.create_table(
        'invoices',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('branch_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('branches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('member_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('members.id', ondelete='CASCADE'), nullable=False),
        sa.Column('subscription_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('member_subscriptions.id'), nullable=True),
        sa.Column('invoice_number', sa.String(50), nullable=False),
        sa.Column('subtotal', sa.Numeric(10, 2), nullable=False),
        sa.Column('discount_amount', sa.Numeric(10, 2), server_default='0.00', nullable=False),
        sa.Column('tax_amount', sa.Numeric(10, 2), server_default='0.00', nullable=False),
        sa.Column('total_amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('paid_amount', sa.Numeric(10, 2), server_default='0.00', nullable=False),
        sa.Column('balance_due', sa.Numeric(10, 2), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(20), server_default='UNPAID', nullable=False),
        sa.Column('issued_by_user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.UniqueConstraint('tenant_id', 'invoice_number', name='uq_tenant_invoice_number')
    )

    # 9. Cash Registers Table
    op.create_table(
        'cash_registers',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('branch_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('branches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('opened_by_user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('closed_by_user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('shift_name', sa.String(50), server_default='MORNING', nullable=False),
        sa.Column('opening_balance', sa.Numeric(10, 2), server_default='0.00', nullable=False),
        sa.Column('closing_cash_counted', sa.Numeric(10, 2), nullable=True),
        sa.Column('expected_cash_calculated', sa.Numeric(10, 2), nullable=True),
        sa.Column('discrepancy_amount', sa.Numeric(10, 2), server_default='0.00', nullable=False),
        sa.Column('discrepancy_note', sa.Text(), nullable=True),
        sa.Column('shift_status', sa.String(20), server_default='OPEN', nullable=False),
        sa.Column('opened_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('closed_at', sa.DateTime(timezone=True), nullable=True)
    )

    # 10. Payments Table
    op.create_table(
        'payments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('branch_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('branches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('invoice_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('invoices.id', ondelete='CASCADE'), nullable=False),
        sa.Column('cash_register_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('cash_registers.id'), nullable=True),
        sa.Column('payment_mode', sa.String(20), nullable=False),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('reference_transaction_id', sa.String(100), nullable=True),
        sa.Column('status', sa.String(20), server_default='SUCCESS', nullable=False),
        sa.Column('collected_by_user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False)
    )

    # 11. Attendance Logs Table
    op.create_table(
        'attendance_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('branch_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('branches.id', ondelete='CASCADE'), nullable=False),
        sa.Column('member_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('members.id', ondelete='CASCADE'), nullable=False),
        sa.Column('checkin_time', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('checkout_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('method', sa.String(20), server_default='DYNAMIC_QR', nullable=False),
        sa.Column('decision', sa.String(30), server_default='ALLOWED', nullable=False),
        sa.Column('rejection_reason', sa.String(100), nullable=True),
        sa.Column('verified_by_user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('device_identifier', sa.String(50), nullable=True)
    )

    # 12. Enable Row-Level Security (RLS) on Tenant Tables
    tables_with_rls = [
        'branches', 'users', 'members', 'membership_plans', 
        'member_subscriptions', 'invoices', 'cash_registers', 
        'payments', 'attendance_logs'
    ]
    for tbl in tables_with_rls:
        op.execute(f"ALTER TABLE {tbl} ENABLE ROW LEVEL SECURITY;")
        op.execute(f"""
            DO $$ BEGIN
                CREATE POLICY tenant_isolation_{tbl} ON {tbl}
                    FOR ALL
                    USING (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::UUID)
                    WITH CHECK (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::UUID);
            EXCEPTION WHEN duplicate_object THEN null; END $$;
        """)

def downgrade() -> None:
    tables = [
        'attendance_logs', 'payments', 'cash_registers', 'invoices',
        'member_subscriptions', 'membership_plans', 'members',
        'users', 'branches', 'tenants'
    ]
    for tbl in tables:
        op.drop_table(tbl)
