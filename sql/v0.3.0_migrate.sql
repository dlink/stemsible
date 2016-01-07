-- v0.3.0 migrate script

set foreign_key_checks = 0;


-- Create likes Tab

create table likes (
  id                 integer unsigned not null auto_increment primary key,
  user_id            integer unsigned not null ,
  message_id         integer unsigned not null ,

  created            datetime         not null ,
  last_updated       timestamp        not null 
        default current_timestamp on update current_timestamp,

  foreign key (user_id) references users (id),
  foreign key (message_id) references messages (id),
  constraint user_id_message_id unique (user_id, message_id)
) 
engine InnoDB default charset=utf8;
;
show warnings;

create trigger likes_create before insert on likes
   for each row set new.created = now();

desc likes;

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



set foreign_key_checks = 1;

