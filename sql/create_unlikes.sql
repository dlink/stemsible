-- Create unlikes table

-- Used to record when a user unlikes a message that they previously liked
-- unlink the likes table, this table does not have a unique constraint
-- on user_id, message_id

create table unlikes (
  id                 integer unsigned not null auto_increment primary key,
  user_id            integer unsigned not null ,
  message_id         integer unsigned not null ,

  created            datetime         not null ,
  last_updated       timestamp        not null 
        default current_timestamp on update current_timestamp,

  foreign key (user_id) references users (id),
  foreign key (message_id) references messages (id)
) 
engine InnoDB default charset=utf8;
;
show warnings;

create trigger unlikes_create before insert on unlikes
   for each row set new.created = now();

desc unlikes;
