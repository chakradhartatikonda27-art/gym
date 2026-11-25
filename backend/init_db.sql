-- Siyantech Gym OS - Production Schema Initialization with Seed Data
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. ENUMS
DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('SUPER_ADMIN', 'GYM_OWNER', 'BRANCH_MANAGER', 'RECEPTIONIST', 'TRAINER');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE member_status AS ENUM ('LEAD', 'ACTIVE', 'EXPIRED', 'FROZEN', 'SUSPENDED');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE plan_interval AS ENUM ('DAYS', 'MONTHS', 'YEARS');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE subscription_status AS ENUM ('PENDING_PAYMENT', 'ACTIVE', 'FROZEN', 'EXPIRED', 'CANCELLED');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE payment_mode AS ENUM ('CASH', 'UPI', 'CREDIT_CARD', 'DEBIT_CARD', 'NET_BANKING');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE invoice_status AS ENUM ('DRAFT', 'UNPAID', 'PARTIALLY_PAID', 'PAID', 'CANCELLED');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE checkin_method AS ENUM ('DYNAMIC_QR', 'MANUAL_OVERRIDE', 'RFID', 'BIOMETRIC', 'FACE_RECOGNITION');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE attendance_decision AS ENUM ('ALLOWED', 'DENIED_EXPIRED', 'DENIED_FROZEN', 'DENIED_DUES_EXCEEDED', 'DENIED_INVALID_TIMING');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE shift_status AS ENUM ('OPEN', 'CLOSED', 'DISCREPANCY_FLAGGED');
EXCEPTION WHEN duplicate_object THEN null; END $$;

-- 2. TABLES
CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_name VARCHAR(150) NOT NULL,
    subdomain VARCHAR(50) UNIQUE NOT NULL,
    contact_email VARCHAR(150) NOT NULL,
    contact_phone VARCHAR(20) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    tier VARCHAR(20) NOT NULL DEFAULT 'STARTER',
    whatsapp_monthly_quota INT NOT NULL DEFAULT 500,
    whatsapp_used_quota INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS branches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    branch_name VARCHAR(100) NOT NULL,
    branch_code VARCHAR(10) NOT NULL,
    address_line TEXT NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    gstin VARCHAR(20),
    max_capacity INT DEFAULT 150,
    allow_grace_period_days INT NOT NULL DEFAULT 2,
    max_allowed_dues_threshold NUMERIC(10, 2) NOT NULL DEFAULT 500.00,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_tenant_branch_code UNIQUE (tenant_id, branch_code)
);

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    branch_id UUID REFERENCES branches(id) ON DELETE SET NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'RECEPTIONIST',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_tenant_user_email UNIQUE (tenant_id, email),
    CONSTRAINT uq_tenant_user_phone UNIQUE (tenant_id, phone)
);

CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    branch_id UUID NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(150),
    gender VARCHAR(10),
    lead_source VARCHAR(50) DEFAULT 'WALK_IN',
    fitness_goal VARCHAR(100),
    follow_up_date DATE,
    assigned_to_user_id UUID REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'NEW',
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    home_branch_id UUID NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    member_code VARCHAR(30) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(150),
    gender VARCHAR(10) NOT NULL,
    date_of_birth DATE,
    profile_photo_url TEXT,
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    has_medical_conditions BOOLEAN NOT NULL DEFAULT FALSE,
    medical_notes TEXT,
    waiver_signed BOOLEAN NOT NULL DEFAULT TRUE,
    waiver_signed_at TIMESTAMPTZ DEFAULT NOW(),
    current_status member_status NOT NULL DEFAULT 'ACTIVE',
    last_attended_at TIMESTAMPTZ,
    converted_from_lead_id UUID REFERENCES leads(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_tenant_member_code UNIQUE (tenant_id, member_code),
    CONSTRAINT uq_tenant_member_phone UNIQUE (tenant_id, phone)
);

CREATE TABLE IF NOT EXISTS membership_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    plan_name VARCHAR(100) NOT NULL,
    interval_unit plan_interval NOT NULL DEFAULT 'MONTHS',
    interval_value INT NOT NULL,
    base_price NUMERIC(10, 2) NOT NULL,
    joining_fee NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    tax_percentage NUMERIC(5, 2) NOT NULL DEFAULT 18.00,
    max_freeze_days INT NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS member_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    branch_id UUID NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    member_id UUID NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    plan_id UUID NOT NULL REFERENCES membership_plans(id),
    start_date DATE NOT NULL,
    original_end_date DATE NOT NULL,
    current_end_date DATE NOT NULL,
    total_frozen_days INT NOT NULL DEFAULT 0,
    status subscription_status NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS subscription_freezes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    subscription_id UUID NOT NULL REFERENCES member_subscriptions(id) ON DELETE CASCADE,
    freeze_start_date DATE NOT NULL,
    freeze_end_date DATE NOT NULL,
    days_frozen INT NOT NULL,
    reason TEXT NOT NULL,
    approved_by_user_id UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    branch_id UUID NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    member_id UUID NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    subscription_id UUID REFERENCES member_subscriptions(id),
    invoice_number VARCHAR(50) NOT NULL,
    subtotal NUMERIC(10, 2) NOT NULL,
    discount_amount NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    tax_amount NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    total_amount NUMERIC(10, 2) NOT NULL,
    paid_amount NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    balance_due NUMERIC(10, 2) NOT NULL,
    due_date DATE,
    status invoice_status NOT NULL DEFAULT 'UNPAID',
    issued_by_user_id UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_tenant_invoice_number UNIQUE (tenant_id, invoice_number)
);

CREATE TABLE IF NOT EXISTS cash_registers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    branch_id UUID NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    opened_by_user_id UUID NOT NULL REFERENCES users(id),
    closed_by_user_id UUID REFERENCES users(id),
    shift_name VARCHAR(50) NOT NULL DEFAULT 'MORNING',
    opening_balance NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    closing_cash_counted NUMERIC(10, 2),
    expected_cash_calculated NUMERIC(10, 2),
    discrepancy_amount NUMERIC(10, 2) DEFAULT 0.00,
    discrepancy_note TEXT,
    shift_status shift_status NOT NULL DEFAULT 'OPEN',
    opened_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    closed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    branch_id UUID NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
    cash_register_id UUID REFERENCES cash_registers(id),
    payment_mode payment_mode NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    reference_transaction_id VARCHAR(100),
    status VARCHAR(20) NOT NULL DEFAULT 'SUCCESS',
    collected_by_user_id UUID NOT NULL REFERENCES users(id),
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS expenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    branch_id UUID NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    cash_register_id UUID REFERENCES cash_registers(id),
    category VARCHAR(50) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    payment_mode payment_mode NOT NULL DEFAULT 'CASH',
    paid_to VARCHAR(100) NOT NULL,
    notes TEXT,
    logged_by_user_id UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS attendance_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    branch_id UUID NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    member_id UUID NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    checkin_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    checkout_time TIMESTAMPTZ,
    method checkin_method NOT NULL DEFAULT 'DYNAMIC_QR',
    decision attendance_decision NOT NULL DEFAULT 'ALLOWED',
    rejection_reason VARCHAR(100),
    verified_by_user_id UUID REFERENCES users(id),
    device_identifier VARCHAR(50)
);

-- 3. SEED INITIAL TENANT, BRANCH, OWNER, AND DEFAULT PLANS
INSERT INTO tenants (id, business_name, subdomain, contact_email, contact_phone, tier)
VALUES ('c0a8012e-8f20-4b8c-b062-b9d997678f21', 'Fitness Republic Club', 'fitrepublic', 'admin@fitrepublic.com', '+919849011223', 'PRO')
ON CONFLICT DO NOTHING;

INSERT INTO branches (id, tenant_id, branch_name, branch_code, address_line, city, state, pincode, gstin)
VALUES ('d1b9123f-9a31-4c9d-c173-caea08789032', 'c0a8012e-8f20-4b8c-b062-b9d997678f21', 'Jubilee Hills Flagship', 'JH01', 'Road No 36, Jubilee Hills', 'Hyderabad', 'Telangana', '500033', '36AABCF1234F1Z1')
ON CONFLICT DO NOTHING;

-- Seed Owner (Password: Admin@123 -> bcrypt hash)
INSERT INTO users (id, tenant_id, branch_id, full_name, email, phone, password_hash, role)
VALUES (
    'e2c9234a-0b42-4d8e-d284-dbfa19890143',
    'c0a8012e-8f20-4b8c-b062-b9d997678f21',
    'd1b9123f-9a31-4c9d-c173-caea08789032',
    'Kiran Reddy',
    'owner@fitrepublic.com',
    '+919849011223',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', -- Admin@123
    'GYM_OWNER'
) ON CONFLICT DO NOTHING;

-- Seed Receptionist (Password: Reception@123)
INSERT INTO users (id, tenant_id, branch_id, full_name, email, phone, password_hash, role)
VALUES (
    'f3d0345b-1c53-4e9f-e395-ec0b20901254',
    'c0a8012e-8f20-4b8c-b062-b9d997678f21',
    'd1b9123f-9a31-4c9d-c173-caea08789032',
    'Priya Sharma',
    'reception@fitrepublic.com',
    '+919849055667',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', -- Reception@123
    'RECEPTIONIST'
) ON CONFLICT DO NOTHING;

-- Seed Plans
INSERT INTO membership_plans (id, tenant_id, plan_name, interval_unit, interval_value, base_price, tax_percentage, max_freeze_days)
VALUES 
    ('11111111-1111-1111-1111-111111111111', 'c0a8012e-8f20-4b8c-b062-b9d997678f21', 'Annual Strength & Cardio', 'YEARS', 1, 12711.00, 18.00, 30),
    ('22222222-2222-2222-2222-222222222222', 'c0a8012e-8f20-4b8c-b062-b9d997678f21', 'Half-Yearly Fitness', 'MONTHS', 6, 7626.27, 18.00, 15),
    ('33333333-3333-3333-3333-333333333333', 'c0a8012e-8f20-4b8c-b062-b9d997678f21', 'Quarterly Pro', 'MONTHS', 3, 4236.44, 18.00, 7),
    ('44444444-4444-4444-4444-444444444444', 'c0a8012e-8f20-4b8c-b062-b9d997678f21', 'Monthly Starter', 'MONTHS', 1, 1694.07, 18.00, 0)
ON CONFLICT DO NOTHING;
