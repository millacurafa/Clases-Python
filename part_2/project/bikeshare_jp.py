import time
import pandas as pd
import numpy as np
import datetime as dt
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


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
    while True:
        city = input(
            'Choose a city from the following list: {chicago, new york city, washington} \n ').lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            'Choose a month from the following list: {all, jan, feb, mar, apr, jun, jul, aug, sep, oct, nov, dec} \n').lower()
        if month in ['all', 'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
            break
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            'Choose a day from the following list: {all, mon, tue, wed, thu, fri, sat, sun} \n').lower()
        if day in ['all', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']:
            break
    print('-'*40)
    print(city, month, day)
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
    df['Start Time'] = pd.to_datetime(
        df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    df['Time'] = df['Start Time'].dt.time
    dff = df[(df['Day'].str.lower() == day) &
             (df['Month'].str.lower() == month)]
    return dff


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    most_common_month = df.groupby('Month').count.index.max()
    most_common_day = df.groupby('Day').count.index.max()
    # TO DO: display the most common month
    print(most_common_month)
    # TO DO: display the most common day of week
    print(most_common_day)
    # TO DO: display the most common start hour
    #print(most_common_start_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    most_common_start_station = df.groupby('Start Station').count().index.max()
    most_common_end_station = df.groupby('End Station').count().index.max()
    most_common_combination = df.groupby(
        'Start Station', 'End Station').count().index.max()
    # TO DO: display most commonly used start station
    print('The most common Start Station is: ' + most_common_start_station)
    # TO DO: display most commonly used end station
    print('The most common End Station is: ' + most_common_end_station)
    # TO DO: display most frequent combination of start station and end station trip
    print('The most common Combination Station is: ' +
          str(most_common_combination))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()
    # TO DO: display total travel time
    print('The total travel time is: ' + str(total_travel_time))
    # TO DO: display mean travel time
    print('The mean travel time is: ' + str(mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # TO DO: Display counts of user types
    count_user_type = df.groupby('User Type').size()
    print('The counts of users types are: ' + str(count_user_type))
    # TO DO: Display counts of gender
    count_gender_type = df.groupby('Gender').size()
    print('The counts of users gender type is: ' + str(count_gender_type))
    # TO DO: Display earliest, most recent, and most common year of birth
    earliest_year_birth = df['Birth Year'].min()
    most_recent_year_birth = df['Birth Year'].max()
    most_common_year_birth = df.groupby('Birth Year').count().index.max()
    print('The earliest year of birth is: {}, \n the most recent year of birht is: {} \n and the most common year of birth is: {}'.format(
        str(earliest_year_birth), str(most_recent_year_birth), str(most_common_year_birth)))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
