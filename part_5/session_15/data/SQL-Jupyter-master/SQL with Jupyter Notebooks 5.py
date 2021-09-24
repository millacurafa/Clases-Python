# Jupyter notebooks with SQL queries
# GROUP BY and ORDER BY...

# NOTE: GROUP BY comes after WHERE, before ORDER BY, LIMIT

# Loading the SQL extension...
%load_ext sql

# Connecting to sample MySQL dataset via..
%sql mysql://studentuser:studentpw@mysqlserver/dognitiondb

# Designate this as the default database for queries this session...
%sql USE dognitiondb;

# Sample query with group by... Note that we are able to use aliases in group by in MySQL/Jupyter
# but this is not the case for all database systems.
%%sql
SELECT test_name, MONTH(created_at) AS Month, COUNT(created_at) AS Num_Completed_Tests
FROM complete_tests
GROUP BY test_name, Month
ORDER BY test_name ASC, Month ASC;

# Top 10 gender-breed group categories by dog count...
%%sql
SELECT gender, breed_group, COUNT(DISTINCT dog_guid) AS dog_count
FROM dogs
GROUP BY gender, breed_group
ORDER BY dog_count DESC
LIMIT 10;

# Same query as above but with column # shorthand in group by/sort by...
%%sql
SELECT gender, breed_group, COUNT(DISTINCT dog_guid) AS dog_count
FROM dogs
GROUP BY 1, 2
ORDER BY 3 DESC
LIMIT 10;

# HAVING clause works like WHERE but for grouped/aggregated data...
# For example, show only groups with at least 20 records: HAVING COUNT(field)>=20

# For the following, note that the record-level WHERE clause could also have been expressed
# as a HAVING clause for this case: HAVING ISNULL(breed_group) = FALSE
%%sql
SELECT gender, breed_group, COUNT(DISTINCT dog_guid) AS dog_count
FROM dogs
WHERE breed_group!=""
GROUP BY 1, 2
HAVING dog_count >= 1000
ORDER BY 3 DESC
LIMIT 10;

# Get a count of users by state/zip for the U.S. market...
%%sql
SELECT state, zip, COUNT(DISTINCT user_guid) as count
FROM users
WHERE country = "US"
GROUP BY state, zip
ORDER BY state ASC, zip DESC;

# Top 10 U.S. user zip codes...
%%sql
SELECT state, zip, COUNT(DISTINCT user_guid) as count
FROM users
WHERE country = "US" AND state != "N/A"
GROUP BY state, zip
HAVING count >= 5
ORDER BY count DESC
LIMIT 10;
