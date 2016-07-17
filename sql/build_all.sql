-- This script destroys and recreates a working Stemsible Database

-- Drop all tables
-- -- Children first

drop table if exists messages;
drop table if exists follows;
drop table if exists grades;
drop view  if exists user_schools_primary;
drop view  if exists user_schools_primary_ids;
drop table if exists user_schools;
drop table if exists users;
drop table if exists schools;
drop table if exists school_districts;
drop table if exists addresses;

drop table if exists school_relationships;
drop table if exists address_types;

-- Create all tables
-- -- Parents First

source create_address_types.sql;
source create_school_relationships.sql;

source create_addresses.sql;
source create_school_districts.sql;
source create_schools.sql;
source create_users.sql;
source create_user_schools.sql;
source create_user_schools_primary_ids_view.sql;
source create_user_schools_primary_view.sql;
source create_grades.sql;
source create_follows.sql;
source create_messages.sql;

-- Load Test Data
source load_test_data.sql;
