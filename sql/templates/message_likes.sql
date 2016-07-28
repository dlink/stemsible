select
   l.id,
   l.user_id,
   concat_ws(' ', u.first_name, u.last_name) as user_fullname,
   l.message_id,
   l.created
from
   likes l
   join users u on l.user_id = u.id
where
   l.message_id = %s
order by
   l.created
;
