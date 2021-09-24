# Jupyter notebooks with SQL queries
# Inner joins...

# Loading the SQL extension...
%load_ext sql

# Connecting to sample MySQL dataset via..
%sql mysql://studentuser:studentpw@mysqlserver/dognitiondb

# Designate this as the default database for queries this session...
%sql USE dognitiondb;

# Starting with a query of owners most "surprised" by results according to rating...
# Notes: Specify table.field where ambiguous. Without a WHERE clause this would be
# requesting all cartesian products and would be an extremely long query to run.
%%sql 
SELECT d.dog_guid, d.user_guid, AVG(rating) AS AvgRating, COUNT(r.rating) AS TotalRatings,
d.breed, d.breed_group, d.breed_type
FROM dogs d, reviews r
WHERE d.dog_guid=r.dog_guid AND d.user_guid=r.user_guid
GROUP BY d.user_guid
HAVING TotalRatings >= 10
ORDER BY AvgRating DESC
LIMIT 200;

# Counting unique dog_guids and user_guids in each of the tables...
%sql SELECT COUNT(DISTINCT dog_guid), COUNT(DISTINCT user_guid) FROM dogs;
%sql SELECT COUNT(DISTINCT dog_guid), COUNT(DISTINCT user_guid) FROM reviews;

# Inner join across 3 tables to get dogs and users for a specific test...
%%sql
SELECT dogs.user_guid, dogs.dog_guid, dogs.breed_type, dogs.breed_group
FROM dogs, users, complete_tests c
WHERE dogs.dog_guid = c.dog_guid AND c.user_guid = dogs.user_guid
    AND c.test_name = "Yawn Warm-Up"
LIMIT 20;

# Inner join to select dogs (breed = golden retriever) and users who completed 1+ test...
# For 1+: using a join to see if there is at least one ID match in the test table.
%%sql
SELECT DISTINCT d.user_guid, u.membership_type, d.dog_guid, d.breed
FROM dogs d, complete_tests ct, users u
WHERE d.dog_guid = ct.dog_guid AND d.user_guid = u.user_guid 
	AND d.breed = "golden retriever";

# Inner join to count golden retriever dogs in North Carolina...
%%sql
SELECT COUNT(DISTINCT d.dog_guid) AS TotalDogs
FROM dogs d, users u
WHERE d.user_guid = u.user_guid 
    AND u.state = "NC" AND u.country = "US"
    AND d.breed = "golden retriever";

# By membership type, count of members who submitted 1+ review...	
# For 1+: using a join to see if there is at least one ID match in the reviews table.
%%sql
SELECT membership_type AS MembershipType, COUNT(DISTINCT u.user_guid) AS TotalUsers
FROM users u, reviews r
WHERE u.user_guid = r.user_guid
GROUP BY membership_type;

# Top 3 breeds for dog profiles with activity on website...
%%sql
SELECT breed, COUNT(DISTINCT sa.dog_guid) AS CountActive
FROM dogs d, site_activities sa
WHERE d.dog_guid = sa.dog_guid
    AND ISNULL(sa.script_detail_id) = FALSE
GROUP BY breed
ORDER BY CountActive DESC
LIMIT 3;