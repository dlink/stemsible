
-- drop table if exists messages_flat_new;

create table
   messages_flat_new as
select
   m.id,
   concat_ws(' ',
             u.email,
             u.first_name,
             u.last_name,
             group_concat(distinct s.name separator ' '),
             group_concat(distinct sd.name separator ' '),
             group_concat(distinct a.city separator ' '),
	     -- two leter state code too small for fulltext search
             --   group_concat(distinct a.state separator ' '),
             group_concat(distinct a.zipcode separator ' '),
             m.text
             ) as text
   -- now() as created
from
   messages m
   join users u on m.user_id = u.id
   join user_schools us on u.id = us.user_id
   join schools s on us.school_id = s.id
   join school_districts sd on s.school_district_id = sd.id
   join addresses a on s.address_id = a.id
group by
   m.id
;

-- Add full_text index column
alter table messages_flat_new
   add column FTS_DOC_ID bigint unsigned auto_increment not null primary key
   first
;

alter table messages_flat_new add fulltext (text);

drop table if exists messages_flat;

alter table messages_flat_new rename messages_flat;
