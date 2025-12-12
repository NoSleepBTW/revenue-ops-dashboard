-- INDEX IF NOT EXISTS 1: Transaction Date
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions_data (date);

-- INDEX IF NOT EXISTS 2: Client ID
CREATE INDEX IF NOT EXISTS idx_transactions_client_id ON transactions_data (
  client_id
);

-- INDEX IF NOT EXISTS 3: Card ID
CREATE INDEX IF NOT EXISTS idx_transactions_card_id ON transactions_data (
  card_id
);

-- INDEX IF NOT EXISTS 4: Merchant Category Code (MCC)
CREATE INDEX IF NOT EXISTS idx_transactions_mcc ON transactions_data (mcc);

-- INDEX IF NOT EXISTS 5: Composite (Date & Client)
CREATE INDEX IF NOT EXISTS idx_transactions_date_client_id
ON transactions_data (date, client_id);
