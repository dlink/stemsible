
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

create trigger user_statuses_create before insert on user_statuses
   for each row set new.created = now()
;

load data local infile 'data/user_statuses.csv' into table user_statuses
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

desc user_statuses;

