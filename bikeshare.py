# Python script that imports the data and answer interesting questions about it
# by computing descriptive statistics.
# The script takes in raw input to create an interactive experience in the 
# terminal.
3 to present these statistics.
import time
import pandas as pd
import numpy as np
#import calendar month and day names from calendar
from calendar import day_name, day_abbr, month_name, month_abbr

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
        city = input("Enter city (chicago, new york city, washington): ").strip().lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city entered!")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter name of the month or hit enter for all months: ").strip().title()
        if len(month) > 0:
            if month in month_name:
                if list(month_name).index(month) > 6:
                    print("No data available for ", month)
                else:
                    break
            elif month in month_abbr:
                if list(month_abbr).index(month) > 6:
                    print("No data available for ", month)
                else:
                    month = month_name[list(month_abbr).index(month)]
                    break
            else:
                print("Invalid month name entered!\nYou can enter months in full or abbreviated forms (e.g. January or Jan)")
        else:
            month = "all"
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter name of the day or hit enter for all week days: ").strip().title()

        if len(day) != 0:
            if day in day_name:
                break
            elif day in day_abbr:
                day = day_name[list(day_abbr).index(day)]
                break
            else:
                print("Invalid day name entered!")
                print("You can enter day names in full or abbreviated forms (e.g. Monday or Mon)")
        else:
            day = "all"
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
    df = pd.read_csv(CITY_DATA[city])
    print("Number of records loaded for city [{}]: {:,}".format(city, df.shape[0]))

    # Change data type of start time and end time columns from string to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    df['End Time'] = pd.to_datetime(df['End Time'], format='%Y-%m-%d %H:%M:%S')
    df['Start Month'] = df['Start Time'].dt.month_name()
    df['Start Day'] = df['Start Time'].dt.day_name()

    if month != "all":
         df = df[df['Start Month'] == month]

    if day != "all":
        df = df[df['Start Day'] == day]

    # remove unnamed column number 1
    df.drop(columns=df.columns[0], inplace=True)

    # re-index the DataFrame
    df.index = np.arange(1, df.shape[0]+1)

    if month != "all" or day != "all":
        print("Number of records after applying filter on month [{}] and day [{}]: {:,}".format(month, day, df.shape[0]))

    print('-'*40)
    return df

def display_counts(sr, row_str="{}\t{}", n=1, table=False):
    """
    Displays the counts of a given series.

    Args:
        (Series) sr - Pandas Series to display its value counts
        {str)    row _str - the string that will be used to format the row
                            it must include two curely brackets '{}'
                            the first will be substituted with the value
                            the second will be substituted with the count
                            if the provided string does not meet this condition
                            it will be substituted with the default string
        (int)    n - number of count values to print
        (bool)   table - show table heading or not
    """
    # check that provided row_str is valid
    if row_str.count("{}") != 2:
        row_str = "{}\t{}"

    # Get value counts of the series
    val_counts = sr.value_counts()

    # Print table heading if required
    if table:
        print("{}\tCount".format(sr.name))

    # Get number of rows to display based on 'n' and the actual length of the series
    if n > 0 and n < len(val_counts):
        r = range(n)
    else:
        r = range(len(val_counts))

    for i in r:
        print(row_str.format(val_counts.index[i], val_counts.values[i]))

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    display_counts(df['Start Month'], "Most common month: {} - Number of trips: {}")
    # display the most common day of week
    display_counts(df['Start Day'], "Most common day: {} - Number of trips: {}")
    # display the most common start hour
    display_counts(df['Start Time'].dt.hour, "Most common hour: {} - Number of trips: {}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    display_counts(df['Start Station'], "Most common Start Station: [{}] - Used {} times")

    # display most commonly used end station
    display_counts(df['End Station'], "Most common End Station: [{}] - Used {} times")

    # display most frequent combination of start station and end station trip
    display_counts(df['Start Station'] + " -> " + df['End Station'], "Most frequent combination Stations: [{}] - Number of trips: {}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() / 60
    print('Total travel time: {:,.2f} minutes'.format(total_travel_time))
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 60
    print('Mean travel time: {:,.2f} minutes'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    display_counts(df['User Type'], n=0, table=True)
    print()

    # Display counts of gender
    if 'Gender' in df:
        display_counts(df['Gender'], n=0, table=True)
        print()

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        # min
        min_birth_year = df['Birth Year'].min()
        print("Earliest year of birth: {}".format(min_birth_year))
        # max
        max_birth_year = df['Birth Year'].max()
        print("Most recent year of birth: {}".format(max_birth_year))
        # most common
        display_counts(df['Birth Year'], "Most common year of birth: {} - {} times")

    print()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df, n=5):
    """
    Displays raw data of given data frame 'n' records at a time
    """
    # ask user if wants to
    show_data = input("Do you want to see 5 lines of raw data? Enter yes or no.\n")
    index = 1
    max_index = df.shape[0] - 1
    while show_data.lower() == "yes":
        # show all columns except the added columns 'Start Month' and 'Start Day'
        # because they are not part of the original raw data
        print(df.loc[index:index+n-1, df.columns[:-2]])
        index += n
        if index > max_index:
            break
        show_data = input("Do you want to see more lines of raw data? Enter yes or no.\n")

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
