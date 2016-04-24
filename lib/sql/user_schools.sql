select
   us.id,
   sr.name as relation,
   s.name as school,
   us.grade
from
   user_schools us
   join schools s on us.school_id = s.id
   join school_relationships sr on us.school_relationship_id = sr.id
where
   user_id = %s
order by
   us.created;