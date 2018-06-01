ALTER TABLE documents
MODIFY name varchar(512) NOT NULL,
MODIFY last_updated_ema BIGINT,
DROP latest_update;