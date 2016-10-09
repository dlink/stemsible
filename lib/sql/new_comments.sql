select
   u.id as user_id,
   u.email   as user_email,
   m.user_id as message_user_id,
   m.id      as message_id,
   m.text    as message_text,
   group_concat(q.comment_id) as comment_ids,
   group_concat(c.text separator '^!^!^') as comment_texts
from
   notify_queue q
   join users u on q.user_id = u.id
   join messages c on q.comment_id = c.id
   join messages m on c.reference_id = m.id
where
   %s
group by
   1, 2, 3, 4, 5
order by
   u.id desc
;
