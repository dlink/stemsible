-- Load test addresses
load data local infile 'test_data/addresses.csv' into table addresses
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;
select * from addresses;

-- Load test school_districts
load data local infile 'test_data/school_districts.csv'
into table school_districts
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;
select * from school_districts;

-- Load test schools
load data local infile 'test_data/schools.csv' into table schools
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;
select * from schools;

-- Load test users
load data local infile 'test_data/users.csv' into table users
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;
select * from users;

-- Load test user_schools
load data local infile 'test_data/user_schools.csv' into table user_schools
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;
select * from user_schools;

-- load test followers
load data local infile 'test_data/follows.csv' into table follows
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;
select * from follows;

-- Load test messages
load data local infile 'test_data/messages.csv' into table messages
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;
select * from messages;

