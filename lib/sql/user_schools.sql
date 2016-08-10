select
   us.id,
   sr.name as relation,
   s.name as school,
   us.grade,
   sd.name as district
from
   user_schools us
   join schools s on us.school_id = s.id
   join school_relationships sr on us.school_relationship_id = sr.id
   join school_districts sd on s.school_district_id = sd.id
where
   user_id = %s
order by
   us.created;
