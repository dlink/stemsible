-- v0.5.0 migration

set foreign_key_checks = 0;

-- Add reference_id to messages table

alter table messages
   drop column reference_id;

