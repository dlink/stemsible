-- The purpose of this view is to create
-- a list of 'primary' user_school ids for each user
-- currently defined as the first one

-- This is used by the user_schools_primary view

create view user_schools_primary_ids as
select
   min(id) as id, user_id
from
   user_schools us
group by
   user_id
;

