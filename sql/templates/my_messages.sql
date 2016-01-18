select
   m.id,
   m.user_id,
   concat_ws(' ', mu.first_name, mu.last_name) as author,
   m.text,
   m.created,
   '' as reason
from
   messages m
   join users mu on m.user_id = mu.id
where
   m.user_id= '<user_id>' and
   m.reference_id is null
order by
   m.id desc
;
