import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore bikeshare data from Chicago, New York City and Washington!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        city = str(input('Which city do you want to review?'))
        city = city.lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print ('We don´t have data for that city, try with chicago, new york city or washington')
        else:    
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = str(input('Any month in particular or all?'))
        month = month.lower()
        if month not in ('january', 'february', 'march', 'april', 'may','june', 'all'):
            print ('Oops, we don´t have data for that month. Please try beetween january and june or all')
        else:
            break
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input('Any day of the week in particular or just all?'))
        if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday', 'sunday', 'all'):
            print ('No data selected, Please type one particular day or all')
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #Convert 'Star time' and 'End time' to datetime and filter month, day of the week
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month:', common_month)

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day:', common_day)

    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    commonly_start_station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:', commonly_start_station)

    # TO DO: display most commonly used end station
    commonly_end_station = df['End Station'].value_counts().idxmax()
    print('Most Commonly used end station:', commonly_end_station)

######## TO DO: display most frequent combination of start station and end station trip #########
    frequent_combination_station = df [['Start Station', 'End Station']].mode().loc[0]
    print('Most frequent combination of start station and end station:', frequent_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
