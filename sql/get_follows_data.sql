select
   u1.username, u2.username, f.choice, f.grade, f.school, f.school_district
from
   follows f
   join users u1 on f.user_id = u1.id
   join users u2 on f.follows_id = u2.id
;