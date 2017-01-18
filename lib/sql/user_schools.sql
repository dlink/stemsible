select
   us.id,
   sr.name as relation,
   s.name as school,
   s.id as school_id,
   us.grade,
   sd.name as district,
   a.address1,
   a.address2,
   a.city,
   a.state,
   a.zipcode,
   a.country
from
   user_schools us
   join schools s on us.school_id = s.id
   join school_relationships sr on us.school_relationship_id = sr.id
   join school_districts sd on s.school_district_id = sd.id
   join addresses a on s.address_id = a.id
where
   user_id = %s
order by
   us.created;
