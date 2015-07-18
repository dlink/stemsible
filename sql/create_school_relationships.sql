set foreign_key_checks = 0;

-- drop table /*! if exists */ school_relationships;

create table school_relationships (
  id                 integer unsigned not null auto_increment primary key,
  code               varchar(20)      not null,
  name               varchar(255)     not null,
  active             boolean          not null,
  created            datetime         not null ,
  last_updated       timestamp        not null 
        default current_timestamp on update current_timestamp
) 
engine InnoDB default charset=utf8;
;

show warnings;

set foreign_key_checks = 1;

create trigger school_relationsihps_create before insert
   on school_relationships
   for each row set new.created = now()
;
desc school_relationships;
