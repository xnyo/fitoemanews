-- all passwords are 'password'
INSERT INTO users(name, surname, email, password, privileges) VALUES
  ('Test', 'User', 'user@emane.ws', '$2b$12$gLD4bJCqcrjd3poLnN/o/.zPgjo2icGqaSPKTVLiv87Jbr4jeS4I6', 2),
  ('Pending', 'User', 'pending@emane.ws', '$2b$12$gLD4bJCqcrjd3poLnN/o/.zPgjo2icGqaSPKTVLiv87Jbr4jeS4I6', 1);
INSERT INTO api_keys(name, key_hash, user_id) VALUES ('test', 'ed9164073f0e6b70baa6ddd798ad304c9d0cb2ac509b4852aa969bf2185ae90e0631f21a732f0bbf87b164dea565b08a9a607025186dd4661e3ca18e2349ecf2', 1)