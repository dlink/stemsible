-- Returns messages based on search

select
  m.id as id,
  m.user_id,
  m.text,
  m.created,
  concat_ws(' - ', msr.role,
            concat_ws(', ', msa.city, msa.state)) as reason,
  concat_ws(' ', mu.first_name, mu.last_name) as author

from
  messages_flat mf
  join messages m on mf.id = m.id
  join users mu on m.user_id = mu.id

  -- see comments in user_message.sql
  join user_schools_primary mus on mu.id = mus.user_id
  join school_relationships msr on mus.school_relationship_id = msr.id
  join schools ms on mus.school_id = ms.id
  join addresses msa on ms.address_id = msa.id

where
  match(mf.text) against ('<search>' in boolean mode)
  and m.reference_id is null

union

select
  mp.id as id,
  mp.user_id,
  mp.text,
  mp.created,
  concat_ws(' - ', msr.role,
            concat_ws(', ', msa.city, msa.state)) as reason,
  concat_ws(' ', mu.first_name, mu.last_name) as author

from
  messages_flat mf
  join messages m on mf.id = m.id
  join messages mp on m.reference_id = mp.id
  join users mu on mp.user_id = mu.id

  -- see comments in user_message.sql
  join user_schools_primary mus on mu.id = mus.user_id
  join school_relationships msr on mus.school_relationship_id = msr.id
  join schools ms on mus.school_id = ms.id
  join addresses msa on ms.address_id = msa.id

where
  match(mf.text) against ('<search>' in boolean mode)

order by
  -- match(mf.text) against ('<search>' in boolean mode) desc
  id desc
;
