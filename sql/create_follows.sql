
create table follows (
  id                 integer unsigned not null auto_increment primary key,
  user_id            integer unsigned not null comment 'They who follows',
  follows_id         integer unsigned not null comment 'Whom they follow',

  -- reasons why they follow:
  choice             boolean,
  grade              boolean,
  school             boolean,
  school_district    boolean,

  active             boolean          not null,
  created            datetime         not null ,
  last_updated       timestamp        not null 
        default current_timestamp on update current_timestamp,

  unique index user_id_follows_id (user_id, follows_id)
) 
engine InnoDB default charset=utf8;
;

show warnings;

create trigger follow_create before insert on follows
   for each row set new.created = now();

desc follows;
