ALTER TABLE users ADD notify_what int DEFAULT 15 NOT NULL,
ADD notify_by int DEFAULT 1 NOT NULL,
ADD notify_all bool DEFAULT TRUE NOT NULL,
ADD telegram_user_id varchar(16) NULL;