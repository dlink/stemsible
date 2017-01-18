-- Messages in <user_id>'s feed

select
   m.id,
   m.user_id,
   concat_ws(' ', mu.first_name, mu.last_name) as author,
   m.text,
   m.created,
   group_concat(distinct(concat_ws(' - ', msr.role,
                         concat_ws(', ', msa.city, msa.state)))
	        separator ' ; ') as reason

from
   schools s
   join user_schools mus on s.id = mus.school_id
   join users mu on mus.user_id = mu.id
   join messages m on mu.id = m.user_id

   -- TO DO: this needs to be refactored -- relies on view on view
   -- to get a single school role, city and stage
   -- 9/9/2016 - remove used of this view
   -- join user_schools_primary mus on mu.id = mus.user_id

   join school_relationships msr on mus.school_relationship_id = msr.id
   join schools ms on mus.school_id = ms.id
   join addresses msa on ms.address_id = msa.id

   left join messages c on m.id = c.reference_id
where
   s.id = <school_id> and
   m.reference_id is null

group by
   1, 2, 3, 4, 5
order by
   -- m.id desc

   -- sort by comment create date (if exists),
   --    otherwise by message create date
   if(max(c.id) is null, m.id, max(c.id)) desc
limit
   100
;
