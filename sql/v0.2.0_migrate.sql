-- v0.1.1 migration

-- Create user_statuses table
set foreign_key_checks = 0;

drop table if exists user_statuses;

create table user_statuses (
  id                 integer unsigned not null auto_increment primary key,
  code               varchar(20)      not null,
  name               varchar(255)     not null,
  description        varchar(255)     ,
  active             boolean          not null,
  created            datetime         not null ,
  last_updated       timestamp        not null 
        default current_timestamp on update current_timestamp
) 
engine InnoDB default charset=utf8
;

show warnings;

set foreign_key_checks = 1;

create trigger user_statuses_create before insert on user_statuses
   for each row set new.created = now()
;

load data local infile 'data/user_statuses.csv' into table user_statuses
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

desc user_statuses;

-- drop username from users table

alter table users drop column username;

-- add status_id to users table

alter table users add column status_id int unsigned after password;
alter table users add constraint fk_status_id foreign key (status_id)
      references user_statuses (id);

-- increase password column to 80

alter table users change column password password varchar(80);

-- Update School Releationships

source create_school_relationships.sql


-- Add constraints on follows

alter table follows add unique user_id_follows_id (user_id, follows_id);
