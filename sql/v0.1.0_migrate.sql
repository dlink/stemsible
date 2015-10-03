-- v0.1.0 migration

alter table users add column password varchar(25) after last_name;