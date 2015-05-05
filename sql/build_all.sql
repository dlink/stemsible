-- This script destroys and recreates a working Stemsible Database

-- Drop all tables

drop table if exists messages;
drop table if exists users;

-- Create all tables
source create_users.sql;
source create_messages.sql;

-- Load Test Data
source load_test_data.sql
