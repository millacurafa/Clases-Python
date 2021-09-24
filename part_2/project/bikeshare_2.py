# -*- coding: utf-8 -*-
"""
    References:
- Udacity - Felipe Millacura's Class of January 17, 2021
- blog.e-shell.org
- pandas.pydata.org
- docs.python.org
- journaldev.com
- kite.com
"""

import time
import pandas as pd
import datetime

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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input('Please, could you write the city of your interest, we have information from: chicago, new york and washington \n>').lower()
        if city in CITY_DATA.keys():
            break
    # get user input for month (all, january, february, ... , june)
    months = [datetime.date(2000, m, 1).strftime('%B').lower() for m in range(1, 7)]
    months.append('all')
    while True:
        month = input('Please, could you write the month you want to check or "all" for all of them \n>').lower()
        if month in months:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = [datetime.date(2021, 1, d).strftime('%A').lower() for d in range(1, 8)]
    days.append('all')
    while True:
        day = input('Please, could you write the day you want to check or "all" for all of them \n>').lower()
        if day in days:
            break
        
    print('-'*40)
    return city, month, day

# get_filters()

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
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if month != 'all':
        # df['month'] = (datetime.datetime.strptime(month, "%B")).month
        df['month'] = df['Start Time'].dt.month.name('%B')

    if day != 'all':
        df['day_of_week'] = df['Start Time'].dt.day_name('%A')

       
    dff = df[(df['day_of_week'].str.lower()==day)&(df['month'].str.lower()==month)]
    return dff

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df.groupby('month').count().index.max()
    print('The most common month is : ',common_month)

    # display the most common day of week
    common_day = df.groupby('day_week').count().index.max()
    print('The most common day of week is: ',common_day)


    # display the most common start hour
    common_shour = df.groupby('time').count().index.max()
    print('The most common Start hour is: ', str(common_shour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_usstation = df.groupby('Start Station').count().index.max()
    print('The most commonly used start station is: ', common_usstation)
   

    # display most commonly used end station
    common_uestation = df.groupby('End Station').count().index.max()
    print('The most commonly used end station is: ', common_uestation)

    # display most frequent combination of start station and end station trip
    common_fcstation = df.groupby(['Start Station','End Station']).count().index.max()
    print('The most frequent combination of start station and end station trip is: ', str(common_fcstation))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tt_time = df['Trip Duration'].sum()
    print('The total travel time is: ', str(tt_time))

    # display mean travel time
    mt_time = df['Trip Duration'].sum()
    print('The mean travel time is: ', str(mt_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    try:
        # Display counts of user types
        user_types = df['User Type'].value_counts()
        print('User types : ', user_types)

        # Display counts of gender
        gender = df['Gender'].value_counts()
        print('User Gender : ', gender)
        # Display earliest, most recent, and most common year of birth
        earliest_yb = df['Birth Year'].min()
        print('The earliest year of birth : ', str(earliest_yb))
        
        mostrecent_yb = df['Birth Year'].max()
        print('The most recent year of birth : ', str(mostrecent_yb))
        
        mostcommon_yb = df['Birth Year'].index().max()
        print('The most common year of birth : ', str(mostcommon_yb))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except KeyError:
        pass

def display_lines(df):
    """
    Asks user if they want to see five more rows.

    """
    
    index = 0
    ans_user = input('Do you like to see five rows of data ? write "yes" or "no" \n>').lower()
    while ans_user == 'yes' and index+5 < df.shape[0]:
        print(df.iloc[index:index+5])
        index +=5
        ans_user = input('Do you like to see another five rows of data ? write "yes" or "no" \n>').lower()


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
