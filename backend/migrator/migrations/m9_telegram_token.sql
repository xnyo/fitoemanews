CREATE TABLE telegram_link_tokens
(
    id int PRIMARY KEY AUTO_INCREMENT,
    token varchar(16) NOT NULL,
    user_id int NOT NULL,
    expire bigint NOT NULL,
    CONSTRAINT telegram_link_tokens_users_id_fk FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX telegram_link_tokens_token_uindex ON telegram_link_tokens (token);
CREATE UNIQUE INDEX telegram_link_tokens_user_id_uindex ON telegram_link_tokens (user_id);
CREATE INDEX telegram_link_tokens_expire_index ON telegram_link_tokens (expire);