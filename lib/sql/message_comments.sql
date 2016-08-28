select
   u.id      as user_id,
   u.email   as user_email,
   m.id      as message_id,
   group_concat(c.id) as comment_ids,
   group_concat(c.text separator '^!^!^') as comment_texts
from
   messages c
   join messages m on c.reference_id = m.id
   join users u on m.user_id = u.id
where
   c.reference_id is not null and
   c.notification is null
   %s
group by
   1, 2, 3
order by
   m.id desc
;
