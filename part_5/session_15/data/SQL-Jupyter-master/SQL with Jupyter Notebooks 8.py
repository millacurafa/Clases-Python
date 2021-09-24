# Jupyter notebooks with SQL queries
# Outer joins...JOIN..ON clause

# Loading the SQL extension...
%load_ext sql

# Connecting to sample MySQL dataset via..
%sql mysql://studentuser:studentpw@mysqlserver/dognitiondb

# Designate this as the default database for queries this session...
%sql USE dognitiondb;

# Here's how to write an INNER join with JOIN...ON syntax:
# NOTE: You can specify "INNER JOIN" for clarity but it's assumed.
%%sql
SELECT d.user_guid AS UID, d.dog_guid AS DID, d.breed
FROM dogs d JOIN complete_tests c ON d.dog_guid=c.dog_guid
WHERE test_name='Yawn Warm-up'
LIMIT 10;

# An outer join example with RIGHT to look at reviewed dogs missing from the dogs table...
%%sql
SELECT r.dog_guid AS rDogID, d.dog_guid AS dDogID, r.user_guid AS rUserID, d.user_guid AS dUserID, AVG(r.rating) AS AvgRating, COUNT(r.rating) AS NumRatings, d.breed, d.breed_group, d.breed_type
FROM dogs d RIGHT JOIN reviews r
  ON r.dog_guid=d.dog_guid AND r.user_guid=d.user_guid
WHERE d.dog_guid IS NULL
GROUP BY r.dog_guid
HAVING NumRatings >= 10
ORDER BY AvgRating DESC;

# Summarizing all dog IDs and # of tests completed (RIGHT JOIN to include 0 tests)...
%%sql
SELECT DISTINCT d.dog_guid AS DogID, COUNT(ct.dog_guid) AS CompleteTests
FROM dogs d LEFT JOIN complete_tests ct ON d.dog_guid = ct.dog_guid
GROUP BY DogID
ORDER BY CompleteTests DESC
LIMIT 10;

# Confirming number of dogs with completed tests...
%%sql
SELECT COUNT(DISTINCT dog_guid)
FROM complete_tests;

# The following query outputs way more records than expected...
# This is because owners can have multiple dogs - but there may also be some duplicate records.
%%sql
SELECT d.breed, u.user_guid, d.user_guid, d.dog_guid
FROM dogs d RIGHT JOIN users u ON u.user_guid = d.user_guid
LIMIT 50;

# Counting total user ID records v. distinct...
# There are about 3x as may records as distinct users in the join output.
%%sql
SELECT COUNT(u.user_guid), COUNT(d.user_guid), COUNT(DISTINCT u.user_guid), COUNT(DISTINCT d.user_guid)
FROM dogs d RIGHT JOIN users u ON u.user_guid = d.user_guid;

# Are there particular User IDs with a lot of records in the join output? 
# Yes, a few have 100s, one has 1000s.
%%sql
SELECT COUNT(u.user_guid) AS Count, u.user_guid
FROM dogs d RIGHT JOIN users u ON u.user_guid = d.user_guid
GROUP BY u.user_guid
ORDER BY Count DESC
LIMIT 10;

# Investigating user ID: ce225842-7144-11e5-ba71-058fbc01cf0b...

# There are 17 duplicate rows for this user in the users table.
%%sql
SELECT COUNT(*)
FROM users
WHERE user_guid = 'ce225842-7144-11e5-ba71-058fbc01cf0b';

# And 26 linked dog records.
%%sql
SELECT COUNT(*)
FROM dogs
WHERE user_guid = 'ce225842-7144-11e5-ba71-058fbc01cf0b';

# Are there users without linked dogs? 
# Yes, there are over 2000 UserIDs with no match in the dogs table.
%%sql
SELECT COUNT(DISTINCT u.user_guid)
FROM users u LEFT JOIN dogs d ON  u.user_guid = d.user_guid
WHERE d.user_guid IS NULL;

# Are there site activity records logged for non-existent dogs?
# Yes, there are 2 dog_guid values with a lot of entries that are not in the dogs table.
%%sql
SELECT DISTINCT sa.dog_guid, COUNT(sa.dog_guid)
FROM site_activities sa LEFT JOIN dogs d ON sa.dog_guid = d.dog_guid
WHERE d.dog_guid IS NULL AND sa.dog_guid IS NOT NULL
GROUP BY sa.dog_guid
LIMIT 10;



