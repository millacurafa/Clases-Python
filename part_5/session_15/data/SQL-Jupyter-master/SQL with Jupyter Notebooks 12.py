# Jupyter notebooks with SQL queries
# Dognition data analysis - impact of testing circumstances on test completion

# Jupyter notebook at: https://mooc-az-18.oit.duke.edu:40026/notebooks/MySQL_Exercise_12_Queries_that_Test_Relationships_Between_Test_Completion_and_Test_Circumstances.ipynb

# Objective: determine time of day, weekday, and user country relation to 
# test completion.

# Loading the SQL extension...
%load_ext sql
# Connecting to sample MySQL dataset via..
%sql mysql://studentuser:studentpw@mysqlserver/dognitiondb
# Designate this as the default database for queries this session...
%sql USE dognitiondb;

# Weekday and time as factors...

# Count of completed tests by day of the week - Sunday has the most, Friday the least.
# Issue with this query: there are some duplicate dog_guids in the dogs table...
# While using a LEFT JOIN here doesn't exacerbate the issue, it still carries it through.
%%sql
SELECT DAYOFWEEK(ct.created_at) AS nDay, DAYNAME(ct.created_at) AS wDay,
	COUNT(ct.created_at) AS CompleteTests
FROM complete_tests ct LEFT JOIN users u ON ct.user_guid = u.user_guid
	LEFT JOIN dogs d ON d.dog_guid = ct.dog_guid
WHERE (d.exclude = 0 OR d.exclude IS NULL) AND (u.exclude = 0 OR u.exclude IS NULL)
GROUP BY nDay, wDay;

# Rewriting with an INNER JOIN and DISTINCT subquery to address the duplicate dog_guid 
# records in the dogs table...
# Note: switching to an INNER JOIN for complete_tests.
%%sql
SELECT DAYOFWEEK(ct.created_at) AS nDay, DAYNAME(ct.created_at) AS wDay,
	COUNT(ct.created_at) AS CompleteTests
FROM complete_tests ct JOIN (
	SELECT DISTINCT dog_guid
	FROM dogs d JOIN users u ON d.user_guid = u.user_guid
	WHERE (d.exclude = 0 OR d.exclude IS NULL) AND (u.exclude = 0 OR u.exclude IS NULL)
	) IDs ON IDs.dog_guid = ct.dog_guid
GROUP BY nDay, wDay;

# Let's see if this weekday pattern has changed by year..
# In 2013 and 2014 Monday (not Sunday) was actually the highest day. In 2015, Thursdays 
# showed a relative uptick in popularity.
# What we haven't done yet is adjust for time zone...
%%sql
SELECT YEAR(ct.created_at) AS nYear, DAYOFWEEK(ct.created_at) AS nDay, DAYNAME(ct.created_at) AS wDay,
	COUNT(ct.created_at) AS CompleteTests
FROM complete_tests ct JOIN (
	SELECT DISTINCT dog_guid
	FROM dogs d JOIN users u ON d.user_guid = u.user_guid
	WHERE (d.exclude = 0 OR d.exclude IS NULL) AND (u.exclude = 0 OR u.exclude IS NULL)
	) IDs ON IDs.dog_guid = ct.dog_guid
GROUP BY nYear, nDay, wDay
ORDER BY nYear, nDay;

# Given that users live all over the world, an adjustment should be made to timestamps
# so that it reflects local time. Here, looking at just continental U.S. customers and making an 
# assumption to adjust them all to UTC -6 (Central Time) to look at aggregated time of day trends...
# With DATE_SUB(): this shows a much cleaner pattern of Sunday peak and decline through Friday,
# with an uptick on Saturday.
%%sql
SELECT YEAR(ct.DateAdj) AS nYear, DAYOFWEEK(ct.DateAdj) AS nDay, DAYNAME(ct.DateAdj) AS wDay,
	COUNT(ct.DateAdj) AS CompleteTests
FROM (
	SELECT dog_guid, DATE_SUB(created_at, interval 6 hour) AS DateAdj
	FROM complete_tests
	) ct 
	JOIN (
		SELECT DISTINCT dog_guid
		FROM dogs d 
		JOIN (
			SELECT user_guid
			FROM users
			WHERE country = 'US' AND state NOT IN ('AK', 'HI') AND (exclude = 0 OR exclude IS NULL)
			) u ON d.user_guid = u.user_guid
		WHERE (d.exclude = 0 OR d.exclude IS NULL) 
	) IDs ON IDs.dog_guid = ct.dog_guid
GROUP BY nYear, nDay, wDay
ORDER BY nYear, nDay;

# Looking at location factors...
# It's evident from the previous query that the bulk of users are in the continental U.S. 

# U.S. states with the most Dognition users...
# California has by far the most users (greater than 2x NY).
%%sql
SELECT uc.state, COUNT(uc.user_guid) AS UserCount 
FROM (
	SELECT DISTINCT u.user_guid, u.state
	FROM dogs d JOIN users u ON d.user_guid = u.user_guid
	WHERE (d.exclude = 0 OR d.exclude IS NULL) AND (u.exclude = 0 OR u.exclude IS NULL)
		AND u.country = 'US'
	) uc
GROUP BY uc.state
ORDER BY UserCount DESC
LIMIT 5;

# Countries with the most Dognition users...
# There are a lot of NULL and 'N/A' country records - excluding these:
# There are several hundred users from other English-speaking countries (Canada, Australia, UK).
%%sql
SELECT uc.country, COUNT(uc.user_guid) AS UserCount 
FROM (
	SELECT DISTINCT u.user_guid, u.country
	FROM dogs d JOIN users u ON d.user_guid = u.user_guid
	WHERE (d.exclude = 0 OR d.exclude IS NULL) AND (u.exclude = 0 OR u.exclude IS NULL)
		AND u.country IS NOT NULL AND u.country != 'N/A'
	) uc
GROUP BY uc.country
ORDER BY UserCount DESC
LIMIT 10;
	

