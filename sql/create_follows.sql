set foreign_key_checks = 0;

-- drop table /*! if exists */ address_types;

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
        default current_timestamp on update current_timestamp
) 
engine InnoDB default charset=utf8;
;

show warnings;

set foreign_key_checks = 1;

create trigger follow_create before insert on follows
   for each row set new.created = now();

-- load data local infile 'data/follows.csv' into table follows
-- fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

desc follows;
