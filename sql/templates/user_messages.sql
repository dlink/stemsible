select
   m.id,
   m.user_id,
   concat_ws(' ', mu.first_name, mu.last_name) as author,
   m.text,
   m.created,
   concat_ws(' - ', msr.role,
             concat_ws(', ', msa.city, msa.state)) as reason
from
   users u
   join follows f on u.id = f.user_id
   join messages m on f.follows_id = m.user_id
   join users mu on m.user_id = mu.id

   -- TO DO: this needs to be refactored -- relies on view on view
   -- join user_schools mus on mu.id = mus.user_id
   join user_schools_primary mus on mu.id = mus.user_id
   join school_relationships msr on mus.school_relationship_id = msr.id
   join schools ms on mus.school_id = ms.id
   join addresses msa on ms.address_id = msa.id
where
   u.id = '<user_id>' and
   m.reference_id is null
order by
   m.id desc
;
