select
   m.id,
   m.user_id,
   concat_ws(' ', u.first_name, u.last_name) as user_fullname,
   m.text,
   m.created
from
   messages m
   join users u on m.user_id = u.id
where
   m.reference_id = %s
order by
   m.created asc
;
   
   