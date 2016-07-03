-- The purpose of this view is to create
-- a list of 'primary' user_school records for each user
-- currently defined as the first one

-- This is uses the user_schools_primary_ids view

create view user_schools_primary as
select
   us.*
from
   user_schools us
   join user_schools_primary_ids uspi on us.id = uspi.id
;
