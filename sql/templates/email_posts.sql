select
    mu.id as user_id,
    concat_ws(' ', mu.first_name, mu.last_name) as author,
    m.id as message_id,
    m.text,
    m.last_updated
from
    messages m
    join users mu on m.user_id = mu.id
where
    m.reference_id is null and
    m.user_id != %s
order by
    m.id desc
limit
    5
;
