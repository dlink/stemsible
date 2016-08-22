select
   coalesce(num_users, 0) as num_users,
   s.id as school_id,
   s.name,
   s.created
from
   schools s
   left join (
      select
         school_id,
	 count(*) as num_users
      from
         user_schools
      group by
         1
      ) uc on s.id = uc.school_id
where
   address_id = 0
;	    
