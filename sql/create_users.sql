
create table users (
  id            integer unsigned not null auto_increment primary key,
  email         varchar(255)     not null,
  first_name    varchar(255)     ,
  last_name     varchar(255)     ,
  password      varchar(80)      not null,
  status_id     int unsigned     not null,
  created       datetime         not null,
  last_updated  timestamp        not null 
        default current_timestamp on update current_timestamp,

  unique index username (email),
  foreign key (status_id) references user_statuses(id)
) 
engine InnoDB default charset=utf8;
;

show warnings;

create trigger users_create before insert on users
   for each row set new.created = now()
;

desc users;
