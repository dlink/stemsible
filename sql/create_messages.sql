set foreign_key_checks = 0;

-- drop table /*! if exists */ messages;

create table messages (
  id            integer unsigned not null auto_increment primary key,
  user_id       integer unsigned not null,
  text          text,
  created       datetime         not null ,
  last_updated  timestamp        not null 
        default current_timestamp on update current_timestamp,

  foreign key (user_id) references users (id)
) 
engine InnoDB default charset=utf8;
;

show warnings;

create trigger messages_create before insert on messages
   for each row set new.created = now()
;
desc messages;

set foreign_key_checks = 1;
