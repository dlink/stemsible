-- Load test users

load data local infile 'test_data/users.csv' into table users
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

select * from users;

-- Load test messages

load data local infile 'test_data/messages.csv' into table messages
fields terminated by ',' optionally enclosed by '"' ignore 1 lines;

select * from messages;

