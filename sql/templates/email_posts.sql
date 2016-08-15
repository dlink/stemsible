select
    mu.id as user_id,
    concat_ws(' ', mu.first_name, mu.last_name) as author,
    m.text,
    m.last_updated
from
    messages m
    join users mu on m.user_id = mu.id
order by
    m.id desc
limit
    5
;
