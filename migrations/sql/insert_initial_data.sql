-- Insert exchanges
INSERT INTO exchanges (name, is_active, api_config) 
VALUES 
    ('coinex', true, '{"required_fields": ["api_key", "secret_key"]}'::jsonb);

-- Insert subscription plans
INSERT INTO subscription_plans (name, price_monthly, price_yearly, max_robots, max_pairs, features) 
VALUES 
    ('Free', 0, 0, 1, 1, '{"basic_dca": true}'::jsonb),
    ('Pro', 9.99, 99.99, 5, 5, '{"basic_dca": true, "advanced_signals": true}'::jsonb),
    ('Enterprise', 29.99, 299.99, -1, -1, '{"basic_dca": true, "advanced_signals": true, "custom_signals": true}'::jsonb);

-- Insert common trading pairs
INSERT INTO trading_pairs (exchange_id, symbol, base_currency, quote_currency, min_order_size, price_precision, quantity_precision) 
VALUES 
    (1, 'BTC/USDT', 'BTC', 'USDT', 0.0001, 2, 6),
    (1, 'ETH/USDT', 'ETH', 'USDT', 0.001, 2, 5),
    (1, 'BNB/USDT', 'BNB', 'USDT', 0.01, 2, 4);