CREATE TABLE password_reset_tokens
(
    id int PRIMARY KEY AUTO_INCREMENT,
    user_id int not null,
    token varchar(64) not null,
    expire bigint not null,
    CONSTRAINT password_reset_tokens_users_id_fk FOREIGN KEY (user_id) REFERENCES users (id)
);
CREATE UNIQUE INDEX password_reset_tokens_token_uindex ON password_reset_tokens (token);
CREATE UNIQUE INDEX password_reset_tokens_user_id_uindex ON password_reset_tokens (user_id);