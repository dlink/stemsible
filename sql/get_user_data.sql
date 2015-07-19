select
   u.username,
   u.first_name,
   u.last_name,
   sr.code as relation,
   s.name as school,
   us.grade,
   sd.name as school_district,
   concat_ws(', ', a.address1, a.address2, a.city, a.state, a.zipcode,
                   a.country) as school_address,
   concat_ws(', ', a2.address1, a2.address2, a2.city, a2.state, a2.zipcode,
                   a2.country) as school_district_address
from
   users u
   left join user_schools us on u.id = us.user_id
   left join school_relationships sr on us.school_relationship_id = sr.id
   left join schools s on us.school_id = s.id
   left join addresses a on s.address_id = a.id
   left join school_districts sd on s.school_district_id = sd.id
   left join addresses a2 on sd.address_id = a2.id
where
   u.id = 2
\G
