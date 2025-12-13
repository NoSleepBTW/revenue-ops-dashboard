-- Foreign Keys for Referential Integrity
-- Transactions_data -> users_data (client_id)
ALTER TABLE
    transactions_data
ADD
    CONSTRAINT fk_client FOREIGN KEY (client_id) REFERENCES users_data (id);

-- Transactions_data -> cards_data (card_id)
ALTER TABLE
    transactions_data
ADD
    CONSTRAINT fk_card FOREIGN KEY (card_id) REFERENCES cards_data (id);

-- Transactions_data -> mcc_codes (mcc)
ALTER TABLE
    transactions_data
ADD
    CONSTRAINT fk_mcc FOREIGN KEY (mcc) REFERENCES mcc_codes (mcc);

-- train_fraud_data -> transactions_data (id)
ALTER TABLE
    train_fraud_labels
ADD
    CONSTRAINT fk_transaction_fraud FOREIGN KEY (id) REFERENCES transactions_data (id);