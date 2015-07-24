select
   m.id,
   m.user_id,
   concat_ws(' ', mu.first_name, mu.last_name) as author,
   m.text,
   m.created
from
   users u
   join follows f on u.id = f.user_id
   join messages m on f.follows_id = m.user_id
   join users mu on m.user_id = mu.id
where
   u.id = '<user_id>'
order by
   m.id desc
;
