select
    count(*) as total_comments
from
    messages c
where
   c.reference_id is not null and
   c.created >= %s
;
