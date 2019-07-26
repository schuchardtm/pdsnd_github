#!/usr/bin/env python
# coding: utf-8

# In[43]:


import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# In[44]:


#### whether you enter uppercase or lower case the function will output lowercase

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    
    print('Hello! Let\'s explore some US bikeshare data! It will be lots of fun!')
    
    month_dict = {
        'january' : 1,
        'february' : 2,
        'march' : 3,
        'april' : 4,
        'may' : 5,
        'june' : 6,
        'all' : 'all',
        }
   
    day_dict = {
        'monday' : 0,
        'tuesday' : 1,
        'wednesday' : 2,
        'thursday' : 3,
        'friday' : 4,
        'saturday' : 5,
        'sunday' : 6,
        'all' : 'all'
        }
    
    
    while True:
        global city
        valid_cities = ['chicago', 'washington', 'new york city']
        city = input("Which city would you like to explore? Chicago, New York City, and Washington are your only options! ").lower()
        if city not in valid_cities:
            print('Dude come on, enter one of the cities in the list. Spelling actually matters')
            continue
        else:
            break
    
    while True:
        global month
        valid_month = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        month_name = input("Which month would you like to explore? You can enter all, or a specific month from January to June ").lower()
        if month_name not in valid_month:
            print('Seriously? - Stop being stupid and enter a real month. Like I told you, spelling actually matters')
            continue
        else:
            month = month_dict[month_name]
        break
            
    while True:
        global day
        valid_day = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
        upper_day = [day.title() for day in valid_day]
        valid_day += upper_day
        day_name = input("Which day would you like to explore? You can enter all, or a specific day: Monday, Tuesday. . .etc ").lower()
        if day_name not in valid_day:
            print('Ok this is the last time I tell you to put in valid input. Put in an actual day.')
            continue
        else:
            day = day_dict[day_name]
        break
        
        
    print('-'*40)
    return city, month, day


# In[45]:


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
    global df

    df = pd.read_csv(CITY_DATA[city])
    df['month_index'] = pd.DatetimeIndex(df['Start Time']).month
    df['weekday_index'] = pd.DatetimeIndex(df['Start Time']).weekday

    if month == 'all':
        if day == 'all':
            return df
        else:
            df = df.loc[df['weekday_index'] == day]
            return df
    else:
        if day == 'all':
            df = df.loc[df['month_index'] == month]
            return df
        else:
            df = df.loc[(df['month_index'] == month) & (df['weekday_index'] == day)]
            return df
    
    return df


# In[46]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    if len(df) == 0:
        print('There were no riders in {} during your selected time frame.'.format(city.title()))
        
    else:
        
        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()

        # display the most common month
        month_dict = { 1 : 'january', 2 : 'february', 3 : 'march',
                      4 : 'april', 5 : 'may', 6 : 'june', }

        print('The most common month to travel was {}.'.format(month_dict[(np.bincount(df['month_index']).argmax())]))

        # display the most common day of week
        day_dict = day_dict = { 0 : 'monday', 1 : 'tuesday', 2 : 'wednesday',
                               3 : 'thursday', 4 : 'friday', 5 : 'saturday', 6 : 'sunday' }

        print('The most common day to travel was {}.'.format(day_dict[(np.bincount(df['weekday_index']).argmax())]))

        # display the most common start hour
        hour_dict = { 1 : '1AM', 2 : '2AM', 3 : '3AM', 4 : '4AM', 5 : '5AM', 6 : '6AM', 
                     7 : '7AM', 8 : '8AM', 9 : '9AM', 10 : '10AM', 11 : '11AM',
                     12 : '12PM', 13 : '1PM', 14 : '2PM', 15 : '3PM', 16 : '4PM',
                     17 : '5PM', 18 : '6PM', 19 : '7PM', 20 : '8PM', 21 : '9PM',
                     22 : '10PM', 23 : '11PM', 24 : '12AM' }

        print('The most common hour to start a trip was to travel was {}.'              .format(hour_dict[(np.bincount(pd.DatetimeIndex(df['Start Time']).hour).argmax())]))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


# In[47]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    if len(df) == 0:
        print('There were no riders in {} during your selected time frame.'.format(city.title()))
        
    else:
        
        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()

        # display most commonly used start station
        print('The most common start station is {}.'.format(df['Start Station'].value_counts().idxmax()))

        # display most commonly used end station
        print('The most common end station is {}.'.format(df['End Station'].value_counts().idxmax()))


        # display most frequent combination of start station and end station trip
        print('The most common start/end pair of stations is: {}'.format(df.groupby(['Start Station', 'End Station'])        .size().sort_values(ascending=False).idxmax()))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


# In[48]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    if len(df) == 0:
        print('There were no riders in {} during your selected time frame.'.format(city.title()))
        
    else:
        
        print('\nCalculating Trip Duration...\n')
        start_time = time.time()

        # display total travel time
        print('Total travel time for travellers in {} was {} hours'.format(city.title(), sum(df['Trip Duration']/60)))


        # display mean travel time
        print('Mean travel time for travellers in {} was {} minutes'.format(city.title(), ((df['Trip Duration']).mean()/60)))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


# In[49]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    if len(df) == 0:
        print('There were no riders in {} during your selected time frame.'.format(city.title()))
        
    else:
        
        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # Display counts of user types
        print('There were {} subscribers and {} customers in {}.'              .format(df['User Type'].value_counts()['Subscriber'], df['User Type'].value_counts()['Customer'], city.title()))

        # Display counts of gender
        if city == 'washington':
            print('Unfortunately we don\'t have any gender data for {}, so we won\'t be able to display user stats.'                  .format(city.title()))
        
        else:
            print('There were {} male users and {} female users in {}'                  .format(len(df[df['Gender'] == 'Male']), len(df[df['Gender'] == 'Female']), city.title()))

        # Display earliest, most recent, and most common year of birth
        if city == 'washington':
            print('Unfortunately we don\'t have any age data for {}, so we won\'t be able to display user stats.'                  .format(city.title()))
            
        else:        
            print('For customers in {}, the earliest year of birth was {}, the most recent was {}, and the most common was {}.'                  .format(city.title(), int(min(df['Birth Year'].dropna())), int(max(df['Birth Year'].dropna())),                          int(df['Birth Year'].dropna().value_counts().idxmax())))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


# In[50]:


def data_looker(df):
    """Loops through a dataframe and prints slices of 5 rows at a time."""
   
    start = 0
    stop = 5
    
    while True:
        see_data = input('Would you like to see the raw data? Enter yes or no.')
        if see_data == 'yes':
            print(df.iloc[start:stop])
            start = start + 5
            stop = stop + 5
        else:
            break


# In[51]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_looker(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

