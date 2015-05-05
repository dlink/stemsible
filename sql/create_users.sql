set foreign_key_checks = 0;

-- drop table /*! if exists */ users;

create table users (
  id            integer unsigned not null auto_increment primary key,
  username      varchar(25)      not null,
  email         varchar(255)     not null,
  first_name    varchar(255)     ,
  last_name     varchar(255)     ,
  created       datetime         not null ,
  last_updated  timestamp        not null 
        default current_timestamp on update current_timestamp,

  unique index username (username)
) 
engine InnoDB default charset=utf8;
;

show warnings;

set foreign_key_checks = 1;

desc users;
