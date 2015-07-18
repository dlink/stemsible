-- This script destroys and recreates a working Stemsible Database

-- Drop all tables

drop table if exists messages;
drop table if exists users;
drop table if exists schools;
drop table if exists school_districts;
drop table if exists address_types;
drop table if exists addresses;

-- Create all tables

source create_address_types.sql
source create_addresses.sql
source create_schools.sql
source create_school_districts.sql
source create_users.sql;
source create_messages.sql;

-- Load Test Data
source load_test_data.sql
