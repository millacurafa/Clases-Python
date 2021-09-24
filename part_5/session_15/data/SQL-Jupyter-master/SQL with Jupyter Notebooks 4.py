# Jupyter notebooks with SQL queries
# Summarizing data with AVG(), COUNT(), MAX(), MIN(), SUM()
# https://mooc-az-18.oit.duke.edu:40026/notebooks/MySQL_Exercise_04_Summarizing_Your_Data.ipynb

# Loading the SQL extension...
%load_ext sql

# Connecting to sample MySQL dataset via..
%sql mysql://studentuser:studentpw@mysqlserver/dognitiondb

# Designate this as the default database for queries this session...
%sql USE dognitiondb;

# Running a few summaries...
%%sql
SELECT breed
FROM dogs;
SELECT COUNT(breed)
FROM dogs;

%%sql
SELECT COUNT(DISTINCT breed)
FROM dogs;

# Note: Using COUNT(*) counts # of rows in entire table. There is no DISTINCT option. 

# How many dogs completed tests after March 1, 2014?
%%sql
SELECT COUNT(DISTINCT Dog_Guid)
FROM complete_tests
WHERE created_at > '2014-03-01';

# How many dogs have an exclude flag?
%%sql
SELECT COUNT(DISTINCT Dog_Guid)
FROM dogs
WHERE exclude = 1;

# How many NULL values in the exclude field?
%%sql
SELECT SUM(ISNULL(exclude))
FROM dogs;

# Summary of user ratings for the memory game...
%%sql
SELECT test_name AS Test,
AVG(rating) AS Average,
MIN(rating) AS Lowest,
MAX(rating) AS Highest
FROM reviews
WHERE test_name='Memory versus Pointing';

# NOTE TIMESTAMPDIFF function: http://www.w3resource.com/mysql/date-and-time-functions/date-and-time-functions.php
# Example:
%%sql
SELECT script_detail_id AS ID,
TIMESTAMPDIFF(minute, start_time, end_time) AS Duration
FROM exam_answers
LIMIT 10;

# Average amount of time it took users to complete all tests...outputs a single summary value
# Add a WHERE clause to look at average duration for a particular test (test_name)
%%sql
SELECT AVG(TIMESTAMPDIFF(minute, start_time, end_time)) AS AverageDuration
FROM exam_answers;

# Min and Max Duration...
%%sql
SELECT MIN(TIMESTAMPDIFF(minute,start_time, end_time)) AS Min, MAX(TIMESTAMPDIFF(minute,start_time, end_time)) AS Max
FROM exam_answers;

# How many durations calculate as a negative value?
%%sql
SELECT COUNT(TIMESTAMPDIFF(minute,start_time, end_time))
FROM exam_answers
WHERE TIMESTAMPDIFF(minute,start_time, end_time) < 0;

# Pulling these records for a closer look...
%%sql
SELECT *
FROM exam_answers
WHERE TIMESTAMPDIFF(minute,start_time, end_time) < 0
LIMIT 10;

# Average duration for all users when we exclude the negative values...
%%sql
SELECT AVG(TIMESTAMPDIFF(minute, start_time, end_time)) AS AverageDuration
FROM exam_answers
WHERE TIMESTAMPDIFF(minute,start_time, end_time) > 0;







