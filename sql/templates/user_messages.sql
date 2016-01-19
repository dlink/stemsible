select
   m.id,
   m.user_id,
   concat_ws(' ', mu.first_name, mu.last_name) as author,
   m.text,
   m.created,
   concat_ws(' / ',
             if (f.choice, 'friends', null),
             if (f.grade, 'same grade', null),
             if (f.school, 'same school', null),
             if (f.school_district, 'same district', null)) as reason
from
   users u
   join follows f on u.id = f.user_id
   join messages m on f.follows_id = m.user_id
   join users mu on m.user_id = mu.id
where
   u.id = '<user_id>' and
   m.reference_id is null
order by
   m.id desc
;
