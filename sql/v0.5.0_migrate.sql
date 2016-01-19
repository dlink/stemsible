-- v0.5.0 migration

-- Add reference_id to messages table

alter table messages
   add column reference_id integer unsigned after user_id;

