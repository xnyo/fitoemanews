CREATE TABLE activation_tokens
(
    id int PRIMARY KEY AUTO_INCREMENT,
    user_id int NOT NULL,
    token varchar(64) NOT NULL,
    CONSTRAINT activation_tokens_users_id_fk FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX activation_tokens_user_id_uindex ON activation_tokens (user_id);
CREATE UNIQUE INDEX activation_tokens_token_uindex ON activation_tokens (token);