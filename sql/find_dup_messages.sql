-- Problem statement
-- After user creates a new comment, or creates a new post -- if they immediately refresh the page (with Ctrl-R for example), the previous HTML POST data is repeated. And their data update is repeated. You can verify this is dev or staging.

-- This pattern seems to be the solution;
-- https://en.wikipedia.org/wiki/Post/Redirect/Get

-- In the mean time we can remove duplicate entries from the database


-- This query lists dupicate messages (or comments):

select
   m.*
from
   messages m
   join (
      select
         text,
         count(*)
      from
         messages
      group by
         1
      having
         count(*) > 1
   ) m2 on m.text = m2.text
order by
   m.text,
   m.id
;
