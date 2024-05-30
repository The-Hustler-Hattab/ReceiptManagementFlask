create database LLC;

CREATE TABLE operations_receipts (
    id SERIAL PRIMARY KEY,
    file_path VARCHAR(500) NOT NULL,
    total Float NOT NULL,
    sub_total Float NOT NULL,
    tax Float NOT NULL,
    vendor VARCHAR(200) ,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(200) NOT NULL
);
ALTER TABLE operations_receipts
ADD COLUMN company_name VARCHAR(200) NOT NULL;

ALTER TABLE operations_receipts
ADD COLUMN purchased_at TIMESTAMP ;

ALTER TABLE operations_receipts
ADD COLUMN vendor_address VARCHAR(200) ;

ALTER TABLE operations_receipts
ADD COLUMN customer_name VARCHAR(200) ;

ALTER TABLE operations_receipts
ADD COLUMN invoice_id VARCHAR(200) ;

ALTER TABLE operations_receipts
ADD COLUMN spend_type VARCHAR(200) ;

ALTER TABLE operations_receipts
ADD COLUMN sha256 VARCHAR(200) ;


ALTER TABLE LLC.operations_receipts ADD CONSTRAINT operations_receipts_unique UNIQUE KEY (sha256);
