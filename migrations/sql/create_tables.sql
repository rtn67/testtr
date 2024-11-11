-- Drop existing tables if they exist
DROP TABLE IF EXISTS trading_orders CASCADE;
DROP TABLE IF EXISTS trading_signals CASCADE;
DROP TABLE IF EXISTS robots CASCADE;
DROP TABLE IF EXISTS trading_pairs CASCADE;
DROP TABLE IF EXISTS subscription_plans CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS exchanges CASCADE;

-- Create exchanges table
CREATE TABLE exchanges (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT true,
    api_config JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create subscription plans
CREATE TABLE subscription_plans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    price_monthly FLOAT NOT NULL,
    price_yearly FLOAT NOT NULL,
    max_robots INTEGER NOT NULL,
    max_pairs INTEGER NOT NULL,
    features JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    subscription_plan_id INTEGER REFERENCES subscription_plans(id),
    subscription_end_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Create trading pairs table
CREATE TABLE trading_pairs (
    id SERIAL PRIMARY KEY,
    exchange_id INTEGER REFERENCES exchanges(id),
    symbol VARCHAR(20) NOT NULL,
    base_currency VARCHAR(10) NOT NULL,
    quote_currency VARCHAR(10) NOT NULL,
    min_order_size FLOAT,
    price_precision INTEGER,
    quantity_precision INTEGER,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(exchange_id, symbol)
);

-- Create robots table with updated schema
CREATE TABLE robots (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    exchange_id INTEGER REFERENCES exchanges(id),
    trading_pair_id INTEGER REFERENCES trading_pairs(id),
    status VARCHAR(20) DEFAULT 'inactive',
    
    -- Trading Configuration
    initial_investment FLOAT NOT NULL,
    entry_type VARCHAR(20) DEFAULT 'signal',
    
    -- Signal and DCA Configuration
    signal_config JSONB,
    dca_config JSONB,
    
    -- Position Management
    entry_price FLOAT,
    average_entry_price FLOAT,
    current_position FLOAT,
    peak_price FLOAT,
    total_invested FLOAT DEFAULT 0.0,
    unrealized_pnl FLOAT,
    
    -- Order Management
    total_orders INTEGER DEFAULT 0,
    dca_orders_placed INTEGER DEFAULT 0,
    last_order_time TIMESTAMP,
    last_signal_time TIMESTAMP,
    
    -- Exit Configuration
    take_profit FLOAT,
    stop_loss FLOAT,
    trailing_stop FLOAT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create trading signals table
CREATE TABLE trading_signals (
    id SERIAL PRIMARY KEY,
    robot_id INTEGER REFERENCES robots(id),
    signal_type VARCHAR(10) NOT NULL,
    price FLOAT NOT NULL,
    rsi_value FLOAT,
    macd_value JSONB,
    ma_value JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create trading orders table
CREATE TABLE trading_orders (
    id SERIAL PRIMARY KEY,
    robot_id INTEGER REFERENCES robots(id),
    order_type VARCHAR(20) NOT NULL,
    side VARCHAR(4) NOT NULL,
    amount FLOAT NOT NULL,
    price FLOAT NOT NULL,
    total_cost FLOAT NOT NULL,
    status VARCHAR(20) NOT NULL,
    exchange_order_id VARCHAR(100),
    dca_level INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_robots_user ON robots(user_id);
CREATE INDEX idx_robots_status ON robots(status);
CREATE INDEX idx_trading_signals_robot ON trading_signals(robot_id);
CREATE INDEX idx_trading_orders_robot ON trading_orders(robot_id);
CREATE INDEX idx_trading_pairs_symbol ON trading_pairs(symbol);