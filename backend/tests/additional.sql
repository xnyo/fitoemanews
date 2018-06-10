-- all passwords are 'password'
INSERT INTO users(name, surname, email, password, privileges) VALUES
  ('Test', 'User', 'user@emane.ws', '$2b$12$gLD4bJCqcrjd3poLnN/o/.zPgjo2icGqaSPKTVLiv87Jbr4jeS4I6', 2),
  ('Pending', 'User', 'pending@emane.ws', '$2b$12$gLD4bJCqcrjd3poLnN/o/.zPgjo2icGqaSPKTVLiv87Jbr4jeS4I6', 1);