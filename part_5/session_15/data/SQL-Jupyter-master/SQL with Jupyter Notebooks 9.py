# Jupyter notebooks with SQL queries
# Subqueries and derived tables...

# Loading the SQL extension...
%load_ext sql

# Connecting to sample MySQL dataset via..
%sql mysql://studentuser:studentpw@mysqlserver/dognitiondb

# Designate this as the default database for queries this session...
%sql USE dognitiondb;

# Notes: Subqueries can be used in SELECT, WHERE, and FROM clauses. 
# In FROM clauses they create "derived" tables.
# ORDER BY phrases cannot be used within subqueries.
# Subqueries in SELECT/WHERE clauses that return >1 row must 
# be used with operators that handle multiple values, i.e. IN 
# or they'll be limited to outputting 1 row.

# Example: Selecting values that are greater than average ...
%%sql
SELECT *
FROM exam_answers
WHERE test_name = 'Yawn Warm-Up'
AND TIMESTAMPDIFF(minute,start_time,end_time) > (
    SELECT AVG(TIMESTAMPDIFF(minute,start_time,end_time))
    FROM exam_answers
    WHERE TIMESTAMPDIFF(minute,start_time,end_time) > 0 
	AND test_name = 'Yawn Warm-Up'
);

# Examples with IN, NOT IN...
%%sql
SELECT COUNT(*)
FROM exam_answers
WHERE subcategory_name IN ('Puzzles', 'Numerosity', 'Bark Game');

%%sql
SELECT COUNT(*)
FROM dogs
WHERE breed_group NOT IN ('Working','Sporting','Herding');

# Examples with EXISTS, NOT EXISTS. Note: these can ONLY be used in subqueries.

# Selecting records that have/don't have a match in another table...
# This is the same result as an inner join with a GROUP BY but runs quicker.
%%sql
SELECT COUNT(DISTINCT user_guid) AS UserCount
FROM users u
WHERE NOT EXISTS (
    SELECT d.user_guid 
    FROM dogs d
    WHERE d.user_guid = u.user_guid
);

# Join on just distinct ID values with a subquery...
# Counting the number of dog records per distinct user:
%%sql
SELECT uUsers.user_guid, count(*) AS DogRecords
FROM (
	SELECT DISTINCT u.user_guid 
    FROM users u 
	) AS uUsers 
	LEFT JOIN dogs d ON uUsers.user_guid = d.user_guid
GROUP BY uUsers.user_guid
ORDER BY DogRecords DESC;

# There is one user ID with 1819 dog records. Taking a look at these...
%%sql
SELECT *
FROM (
	SELECT DISTINCT u.user_guid 
    FROM users u 
	) AS uUsers 
	LEFT JOIN dogs d ON uUsers.user_guid = d.user_guid
WHERE uUsers.user_guid = 'ce7b75bc-7144-11e5-ba71-058fbc01cf0b';


# Now, ensuring we also include only distinct user records 
# from dogs table as well (there are duplicates in both tables)...
%%sql
SELECT uUsers.user_guid, dUsers.user_guid, count(*) AS DogRecords
FROM (
	SELECT DISTINCT u.user_guid 
    FROM users u 
	) AS uUsers 
	LEFT JOIN (
	SELECT DISTINCT d.user_guid, d.dog_guid, d.breed
	FROM dogs d 
	) AS dUsers
	ON uUsers.user_guid = dUsers.user_guid
GROUP BY uUsers.user_guid
ORDER BY DogRecords DESC;

# Note: FROM subqueries on large datasets much slower than WHERE subqueries.

# Though sometimes it's easier to use a simple inner join with DISTINCT...
# Distinct dogs and their owner location info, WHERE clause:
%%sql
SELECT DISTINCT d.dog_guid, d.user_guid, d.breed_group, u.state, u.zip
FROM dogs d, users u
WHERE breed_group IN ('Working', 'Sporting', 'Herding') 
	AND d.user_guid = u.user_guid;
	
# Instead with an explicit INNER JOIN...
%%sql
SELECT DISTINCT d.dog_guid, d.user_guid, d.breed_group, u.state, u.zip
FROM dogs d INNER JOIN users u ON d.user_guid = u.user_guid
WHERE breed_group IN ('Working', 'Sporting', 'Herding');








