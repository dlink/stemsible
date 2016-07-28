select
    count(*) as total_likes
from
    users u
    join messages m on m.user_id = u.id
    join likes l on l.message_id = m.id
where
   u.id = %s and
   l.created >= %s
;
