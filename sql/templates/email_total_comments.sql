select
    count(*) as total_comments
from
    messages c
    join messages m on c.reference_id = m.id
where
   m.user_id = %s and
   c.created >= %s
;
