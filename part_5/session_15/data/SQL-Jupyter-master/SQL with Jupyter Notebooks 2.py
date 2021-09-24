# Jupyter notebooks with SQL queries
# Filtering with WHERE...

%%sql
SELECT user_guid, free_start_user
FROM users
WHERE free_start_user = 1;

%%sql
SELECT dog_guid
FROM dogs
WHERE dna_tested = 1;

# Note on operators, <> and != can both indicated not equal, 
# use BETWEEN for value range

%%sql
SELECT *
FROM dogs
WHERE weight BETWEEN 10 AND 50;

# Filtering text...
%%sql
SELECT *
FROM dogs
WHERE breed = 'golden retriever';

# Filtering for list inclusion using IN (...)
%%sql
SELECT *
FROM dogs
WHERE breed IN ("golden retriever","poodle");

# % is text wildcard...
%%sql
SELECT *
FROM dogs
WHERE breed LIKE ("s%");

%%sql
SELECT *
FROM users
WHERE state IN ('NC','NY');

# Filtering by date: see http://www.tutorialspoint.com/mysql/mysql-date-time-functions.htm

# Created before 10/15/2015...
%%sql
SELECT *
FROM complete_tests
WHERE created_at < '2015-10-15';

# NULL and NOT NULL..
%%sql
SELECT user_guid
FROM users
WHERE state IS NOT NULL;

# Question 6: How would you retrieve the Dog ID, subcategory_name, 
# and test_name fields, in that order, of the first 10 reviews entered 
# in the Reviews table submitted in 2014?

%%sql
SELECT dog_guid, subcategory_name, test_name
FROM reviews
WHERE YEAR(created_at) = 2014
LIMIT 10;

# Question 7: How would you select all of the User IDs of customers who 
# have female dogs whose breed includes the word "terrier" somewhere 
# in its name?

%%sql
SELECT user_guid
FROM dogs
WHERE gender = 'female' AND breed LIKE ('%terrier%');

# Question 8: How would you select the Dog ID, test name, and 
# subcategory associated with each completed test for the first 100 
# tests entered in October, 2014?

%%sql
SELECT dog_guid, test_name, subcategory_name
FROM complete_tests
WHERE YEAR(created_at) = 2014 
AND MONTH(created_at) = 10
LIMIT 100;
