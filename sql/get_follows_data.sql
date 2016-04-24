select
   u1.email as follower,
   u2.email as follwed,
   f.choice,
   f.grade,
   f.school,
   f.school_district,
   f.active
from
   follows f
   join users u1 on f.user_id = u1.id
   join users u2 on f.follows_id = u2.id
where
   u1.email = 'dvlink@gmail.com'
;