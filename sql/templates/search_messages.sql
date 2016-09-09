-- Returns messages based on search

select
  m.id as id,
  m.user_id,
  concat_ws(' ', mu.first_name, mu.last_name) as author,
  m.text,
  m.created,
  group_concat(distinct(concat_ws(' - ', msr.role,
                         concat_ws(', ', msa.city, msa.state)))
	        separator ' ; ') as reason

from
  messages_flat mf
  join messages m on mf.id = m.id
  join users mu on m.user_id = mu.id
  join user_schools mus on mu.id = mus.user_id
  join school_relationships msr on mus.school_relationship_id = msr.id
  join schools ms on mus.school_id = ms.id
  join addresses msa on ms.address_id = msa.id

where
  match(mf.text) against ('<search>' in boolean mode)
  and m.reference_id is null

group by
  1, 2, 3, 4, 5

union

select
  mp.id as id,
  mp.user_id,
  concat_ws(' ', mu.first_name, mu.last_name) as author,
  mp.text,
  mp.created,
  group_concat(distinct(concat_ws(' - ', msr.role,
                         concat_ws(', ', msa.city, msa.state)))
	        separator ' ; ') as reason

from
  messages_flat mf
  join messages m on mf.id = m.id
  join messages mp on m.reference_id = mp.id
  join users mu on mp.user_id = mu.id
  join user_schools mus on mu.id = mus.user_id
  join school_relationships msr on mus.school_relationship_id = msr.id
  join schools ms on mus.school_id = ms.id
  join addresses msa on ms.address_id = msa.id

where
  match(mf.text) against ('<search>' in boolean mode)

group by
  1, 2, 3, 4, 5

order by
  -- match(mf.text) against ('<search>' in boolean mode) desc
  id desc
;
