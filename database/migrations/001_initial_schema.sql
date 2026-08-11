-- =============================================================================
-- GeMIntel PostgreSQL / MySQL Database Relational Schema Migration (001_initial_schema.sql)
-- =============================================================================

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(64) PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    company_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    mobile VARCHAR(32),
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(32) DEFAULT 'user',
    status VARCHAR(32) DEFAULT 'ACTIVE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subscription_plans (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    duration_days INT NOT NULL,
    features TEXT[],
    status VARCHAR(32) DEFAULT 'ACTIVE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS license_keys (
    id VARCHAR(64) PRIMARY KEY,
    key_code VARCHAR(64) UNIQUE NOT NULL,
    user_id VARCHAR(64) REFERENCES users(id) ON DELETE SET NULL,
    user_email VARCHAR(255) NOT NULL,
    plan_id VARCHAR(64),
    plan VARCHAR(64) NOT NULL,
    amount_paid DECIMAL(10,2) DEFAULT 0,
    status VARCHAR(32) DEFAULT 'ACTIVE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    activation_date TIMESTAMP WITH TIME ZONE,
    expiry_date TIMESTAMP WITH TIME ZONE NOT NULL,
    payment_id VARCHAR(128)
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) REFERENCES users(id) ON DELETE CASCADE,
    plan_id VARCHAR(64) REFERENCES subscription_plans(id),
    plan_name VARCHAR(255) NOT NULL,
    license_key_id VARCHAR(64) REFERENCES license_keys(id),
    payment_id VARCHAR(128),
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    expiry_date TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(32) DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS payments (
    id VARCHAR(128) PRIMARY KEY,
    user_id VARCHAR(64) REFERENCES users(id) ON DELETE SET NULL,
    user_email VARCHAR(255) NOT NULL,
    gateway VARCHAR(64) DEFAULT 'Razorpay',
    plan VARCHAR(64) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    razorpay_order_id VARCHAR(128),
    razorpay_payment_id VARCHAR(128),
    razorpay_signature VARCHAR(255),
    status VARCHAR(32) DEFAULT 'SUCCESS',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    status VARCHAR(32) DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS tenders (
    id VARCHAR(128) PRIMARY KEY,
    bid_number VARCHAR(128) NOT NULL,
    title TEXT NOT NULL,
    organization VARCHAR(255),
    department VARCHAR(255),
    state VARCHAR(128),
    category VARCHAR(128),
    quantity INT DEFAULT 1,
    estimated_value DECIMAL(14,2),
    start_date TIMESTAMP WITH TIME ZONE,
    end_date TIMESTAMP WITH TIME ZONE,
    status VARCHAR(32) DEFAULT 'PUBLISHED',
    source VARCHAR(128) DEFAULT 'GeM Portal Scanner'
);

CREATE TABLE IF NOT EXISTS saved_tenders (
    id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) REFERENCES users(id) ON DELETE CASCADE,
    tender_id VARCHAR(128) REFERENCES tenders(id) ON DELETE CASCADE,
    saved_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admin_logs (
    id VARCHAR(64) PRIMARY KEY,
    action VARCHAR(128) NOT NULL,
    admin_id VARCHAR(64) REFERENCES users(id) ON DELETE SET NULL,
    details TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
