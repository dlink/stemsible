
create table url_previews (
  id               integer unsigned not null auto_increment primary key,
  message_id       integer unsigned not null,
  
  -- this data comes from Embedly oembed()
  author_name      varchar(256)     ,
  provider_name    varchar(256)     not null,
  provider_url     varchar(256)     not null,
  title            varchar(512)     ,
  url              varchar(512)     not null,
  thumbnail_height integer unsigned ,
  thumbnail_width  integer unsigned ,
  thumbnail_url    varchar(1024)    ,
  description      text             ,
  
  created       datetime            not null,
  last_updated  timestamp           not null 
        default current_timestamp on update current_timestamp,

  unique index (message_id, url),
  foreign key (message_id) references messages (id)
) 
engine InnoDB default charset=utf8;
;

show warnings;

create trigger url_previewss_create before insert on url_previews
   for each row set new.created = now()
;

desc url_previews;
