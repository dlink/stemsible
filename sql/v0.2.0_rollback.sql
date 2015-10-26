-- v0.1.1 rollback

alter table users drop foreign key fk_status_id;

alter table users drop column status_id;

drop table user_statuses;

alter table users add column username varchar(25) not null after id;
