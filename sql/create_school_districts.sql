
create table school_districts (
  id                 integer unsigned not null auto_increment primary key,
  code               varchar(20)      not null,
  name               varchar(255)     not null,
  address_id         integer unsigned not null,
  active             boolean          not null,
  created            datetime         not null ,
  last_updated       timestamp        not null 
        default current_timestamp on update current_timestamp,

  foreign key (address_id)         references addresses (id)
) 
engine InnoDB default charset=utf8;
;

show warnings;

create trigger school_districts_create before insert on school_districts
   for each row set new.created = now()
;

load data local infile 'data/school_districts.csv' into table school_districts
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

show warnings;

select * from school_districts;

