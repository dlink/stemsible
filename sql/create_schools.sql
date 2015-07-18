set foreign_key_checks = 0;

-- drop table /*! if exists */ schools;

create table schools (
  id                 integer unsigned not null auto_increment primary key,
  school_district_id integer unsigned not null,
  code               varchar(20)      not null,
  name               varchar(255)     not null,
  address_id         integer unsigned not null,
  active             boolean          not null,
  created            datetime         not null ,
  last_updated       timestamp        not null 
        default current_timestamp on update current_timestamp,

  foreign key (school_district_id) references school_districts (id),
  foreign key (address_id)         references addresses (id)
) 
engine InnoDB default charset=utf8;
;

show warnings;

set foreign_key_checks = 1;

desc schools;
