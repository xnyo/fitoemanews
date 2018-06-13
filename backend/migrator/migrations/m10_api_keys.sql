create table api_keys
(
	id int auto_increment
		primary key,
	name varchar(64) not null,
	key_hash varchar(128) not null,
	user_id int not null,
	constraint api_keys_key_hash_uindex
		unique (key_hash),
	constraint api_keys_users_id_fk
		foreign key (user_id) references users (id)
			on delete cascade
)
;

create index api_keys_user_id_index
	on api_keys (user_id)
;

