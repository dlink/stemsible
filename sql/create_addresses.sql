
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
        default current_timestamp on update current_timestamp,

  foreign key (address_type_id) references address_types (id)

) 
engine InnoDB default charset=utf8;
;

show warnings;

create trigger addresses_create before insert on addresses
   for each row set new.created = now()
;

load data local infile 'data/addresses.csv' into table addresses
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

show warnings;

select * from addresses;
