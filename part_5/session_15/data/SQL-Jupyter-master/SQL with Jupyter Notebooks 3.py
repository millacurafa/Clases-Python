# Jupyter notebooks with SQL queries
# AS, DISTINCT, ORDER BY, .csv statements to modify output...

# Note: if you specify a name containing a space, use quotes

%%sql
SELECT start_time AS 'exam start time'
FROM exam_answers
LIMIT 10;

# DISTINCT to deduplicate...
%%sql
SELECT DISTINCT breed
FROM dogs;

# DISTINCT combinations from multiple columns...
%%sql
SELECT DISTINCT state, city
FROM users
LIMIT 15;

# ORDER BY alphabetical or numeric has default of ASC, specify if DESC

# With multiple sort columns, sort order for each can be set to DESC...
%%sql
SELECT DISTINCT user_guid, state, membership_type
FROM users
WHERE country = "US"
ORDER BY state DESC, membership_type # still ASC
LIMIT 10;

# Save query output as a Python variable and then export as CSV:
##variable_name = %sql [your full query goes here];
##variable_name.csv('output_name.csv')

breed_list = %sql SELECT DISTINCT breed FROM dogs ORDER BY breed;
breed_list.csv('breed_list.csv')

# Get breed list, fixing entries beginning with a "-" via REPLACE...
%%sql
SELECT DISTINCT breed,
REPLACE(breed,'-','') AS breed_fixed
FROM dogs
ORDER BY breed_fixed

# Or to be more selective (i.e. just remove leading "-" cases) with TRIM
%%sql
SELECT DISTINCT breed, TRIM(LEADING '-' FROM breed) AS breed_fixed
FROM dogs
ORDER BY breed_fixed

# Question 4: How would you get a list of all the subcategories of 
# Dognition tests, in alphabetical order, with no test listed more than 
# once (if you do not limit your output, you should retrieve 16 rows)?

%%sql
SELECT DISTINCT subcategory_name
FROM complete_tests
ORDER BY subcategory_name;

# Question 5: How would you create a text file with a list of all the 
# non-United States countries of Dognition customers with no country 
# listed more than once?

foreign = %sql SELECT DISTINCT country FROM users WHERE country != 'US'
foreign.csv('foreign.csv')

# Question 6: How would you find the User ID, Dog ID, and test name of 
# the first 10 tests to ever be completed in the Dognition database?

%%sql
SELECT user_guid, dog_guid, test_name
FROM complete_tests
ORDER BY created_at
LIMIT 10;

# Question 7: How would create a text file with a list of all the 
# customers with yearly memberships who live in the state of North 
# Carolina (USA) and joined Dognition after March 1, 2014, sorted so 
# that the most recent member is at the top of the list?

NCdata = %sql SELECT DISTINCT user_guid, state, created_at FROM users WHERE membership_type = 2 AND state = 'NC' AND country = 'US' AND created_at > '2014_03_01' ORDER BY created_at DESC
NCdata.csv('NCdata.csv')

# Text operations like UPPER, LOWER...
%%sql
SELECT DISTINCT UPPER(breed)
FROM dogs
ORDER BY breed;