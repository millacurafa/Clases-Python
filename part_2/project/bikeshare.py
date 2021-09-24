import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ('chicago', 'new york', 'washington')
    while True:
        city = input('Choose city to analyse: Chicago, New York or Washington? \n> ').lower()
        if city in cities:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    months = tuple(dt.date(2020, i, 1).strftime('%B').lower() for i in range(1,13))
    
    while True:
        month = input('Please enter the month you want to analyse \n> ').lower()
        if month in months:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    
    days =  tuple(dt.date(2020, 6, i).strftime('%A').lower() for i in range(1,8))
    while True:
        day = input('Now enter a day to get your result \n> ').lower()
        if day in days:
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
    for key, value in CITY_DATA.items():
        if city == key:
            df = pd.read_csv(value)
            break
    df['End Time'] = pd.to_datetime(df['End Time'], format='%Y-%m-%d %H:%M:%S')
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    df['Time'] = df['Start Time'].dt.time
    dff = df[(df['Day'].str.lower()== day)&(df['Month'].str.lower()==month)]

    return dff


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    most_common_month = df.groupby('Month').count().index.max()
    most_common_day, most_common_start_hour = df.groupby('Day').count().index.max(), df.groupby('Time').count().index.max()
    # TO DO: display the most common month 
    print('the most common month is: ' + most_common_month)
    # TO DO: display the most common day of week
    print('the most common day of week is: ' + most_common_day)
    # TO DO: display the most common start hour
    print('the most common start hour is: ' + str(most_common_start_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    most_common_start_station, most_common_end_station, most_common_combination = df.groupby('Start Station').count().index.max(), df.groupby('End Station').count().index.max(), df.groupby(['Start Station','End Station']).count().index.max()
    # TO DO: display most commonly used start station
    print('the most common start station is: ' + most_common_start_station)
    # TO DO: display most commonly used end station
    print('the most common end station is: ' + most_common_end_station)
    # TO DO: display most frequent combination of start station and end station trip
    print('the most frequent combination of start station and end station is: ' + str(most_common_combination))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time, total_travel_time, mean_travel_time = time.time(), df['Trip Duration'].sum(), df['Trip Duration'].mean()
    # TO DO: display total travel time
    print('the total travel time is ' + str(total_travel_time))
    # TO DO: display mean travel time
    print('the mean travel time is ' + str(mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try: 
        # TO DO: Display counts of user types
        count_user_type = df.groupby('User Type').size()
        print('the counts of user types are ' + str(count_user_type))
        # TO DO: Display counts of gender
        count_gender = df.groupby('Gender').size()
        print('the count of user gender is ' + str(count_gender))
        # TO DO: Display earliest, most recent, and most common year of birth
        oldest_year_birth, most_recent_year_birth, most_common_year_birth = df['Birth Year'].min(), df['Birth Year'].max(), df.groupby('Birth Year').count().index.max()

        print('the oldest year of birth is: {}, \n the most recent: {} \n and the most common: {}'.format(str(oldest_year_birth), str(most_recent_year_birth), str(most_common_year_birth)))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except KeyError:
        pass

def display_data(df):
    index=0
    user_input=input('would you like to display 5 rows of raw data? ').lower()
    while user_input in ['yes','y','yep','yea'] and index+5 < df.shape[0]:
        print(df.iloc[index:index+5])
        index += 5
        user_input = input('would you like to display more 5 rows of raw data? ').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
