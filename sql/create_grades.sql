set foreign_key_checks = 0;

drop table /*! if exists */ grades;

create table grades (
  id                 integer unsigned not null auto_increment primary key,
  code               varchar(20)      not null,
  name               varchar(255)     not null,
  description        varchar(255)     not null,
  active             boolean          not null,
  created            datetime         not null ,
  last_updated       timestamp        not null 
        default current_timestamp on update current_timestamp
) 
engine InnoDB default charset=utf8;
;

show warnings;

set foreign_key_checks = 1;

create trigger grades_create before insert on grades
   for each row set new.created = now()
;
load data local infile 'data/grades.csv' into table grades
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

select * from grades;
