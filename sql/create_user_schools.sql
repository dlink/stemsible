
create table user_schools (
  id                 integer unsigned not null auto_increment primary key,
  user_id            integer unsigned not null,
  school_relationship_id integer unsigned not null,
  school_id          integer unsigned not null,
  grade              integer signed,
  original_grade     integer signed,
  active             boolean,

  created            datetime         not null ,
  last_updated       timestamp        not null 
        default current_timestamp on update current_timestamp,

  foreign key (user_id) references users (id)
) 
engine InnoDB default charset=utf8;
;

show warnings;

create trigger user_schools_create before insert on user_schools
   for each row set new.created = now()
;

desc user_schools;
