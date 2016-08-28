elect
   u.email,
   -- u.id
   -- m.id as message_id,
   m.text,
   count(*)
from
   likes l
   join messages m on l.message_id = m.id
   join users u on m.user_id = u.id
where
   like.notfication is null
group by
   1,2
;
