-- v0.5.0 migration

set foreign_key_checks = 0;

-- Add reference_id to messages table

alter table messages
   add column reference_id integer unsigned after user_id;

