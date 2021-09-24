# Jupyter notebooks with SQL queries
# Dognition data analysis - factors to boost test completion

# Loading the SQL extension...
%load_ext sql
# Connecting to sample MySQL dataset via..
%sql mysql://studentuser:studentpw@mysqlserver/dognitiondb
# Designate this as the default database for queries this session...
%sql USE dognitiondb;

# Taking a look at factors hypothesized to impact test completion...

# Factor 1: Dog Personality Dimension. Distinct values...
# There are 11 values (including 'None').
%sql SELECT DISTINCT dimension FROM dogs;

# Preliminary query to sum tests completed for each dog, with dimension listed...
%%sql
SELECT COUNT(ct.dog_guid) AS CompleteTests, d.dog_guid, d.dimension
FROM dogs d LEFT JOIN complete_tests ct ON d.dog_guid = ct.dog_guid 
WHERE dimension IS NOT NULL
GROUP BY d.dog_guid, d.dimension
LIMIT 1000;

# Nesting that query to summarize the average completed tests by dimension...
# "Expert" personality has the most, with "Socialite" the least on average.
%%sql
SELECT DogTests.dimension, AVG(DogTests.CompleteTests) AS AvgTestsComplete
FROM (
	SELECT COUNT(ct.dog_guid) AS CompleteTests, d.dog_guid, d.dimension
	FROM dogs d LEFT JOIN complete_tests ct ON d.dog_guid = ct.dog_guid 
	WHERE dimension IS NOT NULL
	GROUP BY d.dog_guid, d.dimension
	LIMIT 1000
	) AS DogTests
GROUP BY DogTests.dimension
ORDER BY AvgTestsComplete DESC;

# There were blank entries with NULL values excluded - confirming
# there are 92 unique dogs with a blank (not NULL) dimension value:
%%sql
SELECT (
    SELECT CASE 
    WHEN dimension = '' THEN 'blank'
    WHEN dimension IS NULL THEN 'NULL'
    ELSE 'Other'
    END) AS Dim, 
    COUNT(DISTINCT dog_guid) AS DogCount
FROM dogs
GROUP BY Dim
ORDER BY DogCount DESC;

# Taking a closer look at those 92 records...
# These dogs all completed less than 20 tests, so wouldn't be 
# assigned a dimension. These should be treated the same as 
# NULL dimension values.
%%sql
SELECT d.*, COUNT(ct.dog_guid) AS CompleteTests
FROM dogs d LEFT join complete_tests ct ON d.dog_guid = ct.dog_guid
WHERE dimension = ''
GROUP BY d.dog_guid
ORDER BY CompleteTests DESC;

# Summarizing average tests by dimension, excluding the 92 records
# and keeping just 0 or NULL value records for the "exclude" field
# supplied by Dognition (exclude=1 indicates testing records)...
# This changes the outcome a bit: "Ace" is the dimension with the
# greatest average tests completed, "Stargazer" has the least. 
# However, there is not a large difference across dimensions.
%%sql
SELECT DogTests.dimension, AVG(DogTests.CompleteTests) AS AvgTestsComplete
FROM (
	SELECT COUNT(ct.dog_guid) AS CompleteTests, d.dog_guid, d.dimension, d.exclude
	FROM dogs d LEFT JOIN complete_tests ct ON d.dog_guid = ct.dog_guid 
	WHERE dimension IS NOT NULL AND dimension != ''
	GROUP BY d.dog_guid
	) AS DogTests
WHERE DogTests.exclude = 0 OR DogTests.exclude IS NULL
GROUP BY DogTests.dimension
ORDER BY AvgTestsComplete DESC;

# So, investigating a 2nd factor: Dog Breed Group...
# There are 7 breed groups, but also NULL (None) and blank values.
%%sql
SELECT breed_group, COUNT(dog_guid)
FROM dogs
GROUP BY breed_group;

# Taking a look at the 16K+ NULL value records. These appear to have
# a breed value (most are "Mixed" of some variety), likely why they haven't 
# been assigned a breed group value.
%%sql
SELECT d.dog_guid, d.breed, d.weight, d.exclude, MIN(ct.created_at), MAX(ct.updated_at), 
    COUNT(ct.created_at) AS CompleteTests
FROM dogs d LEFT JOIN complete_tests ct ON d.dog_guid = ct.dog_guid
WHERE d.breed_group IS NULL
GROUP BY d.dog_guid
LIMIT 100;

# Similarly to the summary by dimension, looking at average tests completed
# by breed group and omitting dogs with <1 complete test.
# "Herding" and "Sporting" are the highest and average 2 more tests 
# completed than the lowest breed group, "Toy".
%%sql
SELECT DogTests.breed_group, AVG(DogTests.CompleteTests) AS AvgTestsComplete,
	COUNT(DogTests.dog_guid) AS DogCount
FROM (
	SELECT COUNT(ct.dog_guid) AS CompleteTests, d.dog_guid, d.breed_group, d.exclude
	FROM dogs d LEFT JOIN complete_tests ct ON d.dog_guid = ct.dog_guid 
	GROUP BY d.dog_guid
	HAVING CompleteTests > 0
	) AS DogTests
WHERE DogTests.exclude = 0 OR DogTests.exclude IS NULL
GROUP BY DogTests.breed_group
ORDER BY AvgTestsComplete DESC;

# Looking also at the breed_type field...
# There are 4 breed types and no NULL values:
%%sql
SELECT breed_type, COUNT(dog_guid)
FROM dogs
GROUP BY breed_type;

# Looking at average tests by breed type (similarly to breed group)...
# Little difference - approx. 0.5 more tests on average for highest v. lowest.
%%sql
SELECT DogTests.PureBreed, AVG(DogTests.CompleteTests) AS AvgTestsComplete,
	COUNT(DogTests.dog_guid) AS DogCount
FROM (
	SELECT COUNT(ct.dog_guid) AS CompleteTests, d.dog_guid, d.exclude,
		CASE WHEN d.breed_type = 'Pure Breed' THEN 'Pure Breed'
		ELSE 'Other'
		END AS PureBreed
	FROM dogs d LEFT JOIN complete_tests ct ON d.dog_guid = ct.dog_guid 
	GROUP BY d.dog_guid
	HAVING CompleteTests > 0
	) AS DogTests
WHERE DogTests.exclude = 0 OR DogTests.exclude IS NULL
GROUP BY DogTests.PureBreed
ORDER BY AvgTestsComplete DESC;

# Factor 3:
# Let's isolate pure breed dogs and categorize by whether or not they 
# are neutered (hypothesis is that owners may be more interested in
# learning about the characteristics of these dogs via completing tests)...

# Isolating pure breed type and adding dog_fixed field...
# Surprisingly, the results show the opposite of what was expected, that
# neutered dogs (pure breed or not) complete 1-2 more tests on average.
%%sql
SELECT DogTests.PureBreed, DogTests.dog_fixed, AVG(DogTests.CompleteTests) AS AvgTestsComplete,
	COUNT(DogTests.dog_guid) AS DogCount
FROM (
	SELECT COUNT(ct.dog_guid) AS CompleteTests, d.dog_guid, d.exclude, d.dog_fixed
		CASE WHEN d.breed_type = 'Pure Breed' THEN 'Pure Breed'
		ELSE 'Other'
		END AS PureBreed
	FROM dogs d LEFT JOIN complete_tests ct ON d.dog_guid = ct.dog_guid 
	GROUP BY d.dog_guid
	HAVING CompleteTests > 0
	) AS DogTests
WHERE DogTests.exclude = 0 OR DogTests.exclude IS NULL
GROUP BY DogTests.PureBreed, DogTests.dog_fixed
ORDER BY AvgTestsComplete DESC;

# Based on averages, breed_group seems like the most promising factor but let's 
# consider whether outliers are playing a disproportionate role...

# Note, average metrics were used here when the median would be more ideal:
# See: https://www.periscopedata.com/blog/medians-in-sql.html
# One way to detect if the averages are impacted greatly by outliers is to include
# a standard deviation field for each average metric with STDDEV:

# Including a standard deviation calculation for breed group...
# Here the coefficients of variation (stddev / mean) are over 70%, not great.
%%sql
SELECT DogTests.breed_group, AVG(DogTests.CompleteTests) AS AvgTestsComplete,
	STDDEV(DogTests.CompleteTests) AS StdDev, COUNT(DogTests.dog_guid) AS DogCount
FROM (
	SELECT COUNT(ct.dog_guid) AS CompleteTests, d.dog_guid, d.breed_group, d.exclude
	FROM dogs d LEFT JOIN complete_tests ct ON d.dog_guid = ct.dog_guid 
	GROUP BY d.dog_guid
	HAVING CompleteTests > 0
	) AS DogTests
WHERE DogTests.exclude = 0 OR DogTests.exclude IS NULL
GROUP BY DogTests.breed_group
ORDER BY AvgTestsComplete DESC;

# Next steps would be to evaluate the median values and do more work to remove outliers, 
# i.e. in Tableau or other tool.


