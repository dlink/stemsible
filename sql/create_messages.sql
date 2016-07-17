
create table messages (
  id            integer unsigned not null auto_increment primary key,
  user_id       integer unsigned not null,
  reference_id  integer unsigned ,
  text          text,

  created       datetime         not null,
  last_updated  timestamp        not null 
        default current_timestamp on update current_timestamp
) 
engine InnoDB default charset=utf8;
;

show warnings;

create trigger messages_create before insert on messages
   for each row set new.created = now()
;

desc messages;
