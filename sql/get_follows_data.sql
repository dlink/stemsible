select
   u1.username as follower,
   u2.username as follwed,
   f.choice,
   f.grade,
   f.school,
   f.school_district,
   f.active
from
   follows f
   join users u1 on f.user_id = u1.id
   join users u2 on f.follows_id = u2.id
;