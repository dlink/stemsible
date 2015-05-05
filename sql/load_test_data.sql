-- Load test users

load data local infile 'data/test_users.csv' into table users
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

select * from users;

-- Load test messages

load data local infile 'data/test_messages.csv' into table messages
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

select * from messages;

