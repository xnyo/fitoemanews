CREATE TABLE notify_herbs
(
    id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user_id int NOT NULL,
    herb_id int NOT NULL,
    CONSTRAINT notify_herbs_users_id_fk FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT notify_herbs_herbs_id_fk FOREIGN KEY (herb_id) REFERENCES herbs (id) ON DELETE CASCADE
);
CREATE INDEX notify_herbs_user_id_index ON notify_herbs (user_id);
CREATE UNIQUE INDEX notify_herbs_user_id_herb_id_uindex ON notify_herbs (user_id, herb_id);