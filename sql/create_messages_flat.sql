
create table messages_flat (
  id             integer unsigned not null auto_increment primary key,
  text           text,
  -- email          varchar(255)     not null,
  -- full_name      varchar(512)     not null,
  -- school_name    varchar(255)     not null,
  -- school_city    varchar(255)     ,
  -- school_state   varchar(2)       ,
  -- school_zipcode varchar(10)      ,
  -- school_district_name varchar(255)     not null,

  created       datetime         not null,

  fulltext (text)
) 
engine InnoDB default charset=utf8;
;

show warnings;

create trigger messages_flat_create before insert on messages_flat
   for each row set new.created = now()
;

desc messages_flat;
