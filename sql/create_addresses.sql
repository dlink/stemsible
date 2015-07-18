set foreign_key_checks = 0;

-- drop table /*! if exists */ addresses;

create table addresses (
  id                 integer unsigned not null auto_increment primary key,
  address_type_id    integer unsigned not null,
  address1           varchar(255)     ,
  address2           varchar(255)     ,
  city               varchar(255)     ,
  state              varchar(2)       ,
  zipcode            varchar(10)      ,
  country            varchar(255)     ,

  created            datetime         not null ,
  last_updated       timestamp        not null 
        default current_timestamp on update current_timestamp
) 
engine InnoDB default charset=utf8;
;

show warnings;

set foreign_key_checks = 1;

desc addresses;
