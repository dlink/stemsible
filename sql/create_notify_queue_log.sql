
create table notify_queue_log (
  id            integer unsigned not null auto_increment primary key,
  user_id       integer unsigned not null,
  comment_id    integer unsigned not null,

  created       datetime         not null, -- not auto update
  last_updated  timestamp        not null 
        default current_timestamp on update current_timestamp,

  unique key (user_id, comment_id),
  foreign key (comment_id) references messages (id)
) 
engine InnoDB default charset=utf8;
;

show warnings;

desc notify_queue_log;
