
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
