select
   m.id,
   m.user_id,
   concat_ws(' ', first_name, last_name) as author,
   m.text,
   m.created
from
   messages m
   join users u on m.user_id = u.id
order by
   m.id desc
;
