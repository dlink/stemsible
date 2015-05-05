select
   m.id,
   concat_ws(' ', u.first_name, u.last_name) as name,
   date(m.created) as date,
   substr(m.text, 1, 50) as text
from
   messages m
   join users u on m.user_id = u.id
;