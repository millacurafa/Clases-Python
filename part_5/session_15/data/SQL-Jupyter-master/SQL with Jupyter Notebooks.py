# Jupyter notebooks with SQL queries

# Note - the ; is not necessary for a single query but is when chaining multiple queries.

# Loading the SQL extension...
%load_ext sql;

# Connecting to sample MySQL dataset via..
%sql mysql://studentuser:studentpw@mysqlserver/dognitiondb

# Designate this as the default database for queries this session...
%sql USE dognitiondb;

# Take a look at which tables are included for this database...
%sql SHOW tables;

# Note: the syntax, which sounds very similar to what you would actually say in the spoken English language, looks like this:
## SHOW columns FROM (enter table name here)
## or if you have multiple databases loaded:
## SHOW columns FROM (enter table name here) FROM (enter database name here)
## or
## SHOW columns FROM databasename.tablename

# The dogs table has 21 columns...
%sql SHOW columns FROM dogs;
# OR for identical output in this case...
%sql DESCRIBE dogs;

# Note: Table or column names with spaces in them need to be surrounded by quotation marks in SQL. 
# MySQL accepts both double and single quotation marks, but some database systems only accept single 
# quotation marks. In all database systems, if a table or column name contains an SQL keyword, the 
# name must be enclosed in backticks instead of quotation marks.

# Note Use %%sql....; for multiple lines of code
# LIMIT to restrict number of rows returned

%%sql
SELECT breed
FROM dogs 
LIMIT 10;

# You can also select rows of data from different parts of the output 
# table, rather than always just starting at the beginning. To do this,
# use the OFFSET clause after LIMIT. The number after the OFFSET clause
# indicates from which row the output will begin querying. Note that 
#the offset of Row 1 of a table is actually 0. Therefore, in the 
#following query:
##SELECT breed
##FROM dogs LIMIT 10 OFFSET 5;
##10 rows of data will be returned, starting at Row 6.
# An alternative way to write the OFFSET clause in the query is:
##SELECT breed
##FROM dogs LIMIT 5, 10;
# In this notation, the offset is the number before the comma, and 
#the number of rows returned is the number after the comma. 

%%sql
SELECT breed
FROM dogs
LIMIT 10
OFFSET 5;

#OR

%%sql
SELECT breed
FROM dogs
LIMIT 5, 10;

# Note: Teradata will use the TOP commmand, not LIMIT

# Multiple column SELECT...
%%sql
SELECT breed, breed_type, breed_group
FROM dogs 
LIMIT 5, 10;

# Wildcard * to select all...
%%sql
SELECT *
FROM reviews
LIMIT 5, 10;

# With a calculated column...
%%sql
SELECT median_iti_minutes, median_iti_minutes / 60
FROM dogs 
LIMIT 5, 10;

# Question 10: How would you retrieve the first 15 rows of data 
# from the dog_guid, subcategory_name, and test_name fields of the 
# Reviews table, in that order?

%%sql
SELECT dog_guid, subcategory_name, test_name
FROM reviews
LIMIT 15;

# Question 11: How would you retrieve 10 rows of data from the 
# activity_type, created_at, and updated_at fields of the 
# site_activities table, starting at row 50? 

%%sql
SELECT activity_type, created_at, updated_at
FROM site_activities
LIMIT 10
OFFSET 49;

# Question 12: How would you retrieve 20 rows of data from all the 
# columns in the users table, starting from row 2000? 

%%sql
SELECT *
FROM users
LIMIT 20
OFFSET 1999;
