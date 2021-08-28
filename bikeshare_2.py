import time
import pandas as pd
import numpy as np
import colorama
from colorama import Fore
from colorama import Style

colorama.init()

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ["all", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
          "november",
          "december"]

days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    month, day = "all", "all"
    count = 0
    print(Fore.CYAN + 'Hello! Let\'s explore some US bikeshare data!' + Style.RESET_ALL)

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        count += 1
        city = str.lower(input("Would you like to see data for chicago , New York or Washington ? ")).strip()
        if city in CITY_DATA.keys():
            response = str.lower(input(f"You have picked {city}, would you wish to change ? Yes , No ")).strip()
            if response != "no":
                continue
            else:
                break
        else:
            if count < 4:
                print("sorry i dint catch that")
            if count == 4:
                print(Fore.RED + "You kidding me , one more chance and am out" + Style.RESET_ALL)
            if count > 5:
                city = ""
                day = month = city
                return city, month, day

        # get user input for month (all, january, february, ... , june)
    count = 0
    while True:
        count += 1
        filter_ = str.lower(input("Would you like to filter by month , day , both or None ? ")).strip()
        if filter_ in ["month", "day", "both", "none"]:
            if filter_ == "month":
                month = get_month()
                break
            if filter_ == "day":
                day = get_day()
                break
            if filter_ == "both":
                month = get_month()
                day = get_day()
                break
            if filter_ == "none":
                month = "all"
                day = "all"
                break
        else:
            if count < 4:
                print("sorry i dint catch that")
            if count == 4:
                print(Fore.RED + "You kidding me , one more chance and am out" + Style.RESET_ALL)
            if count > 5:
                city = ""
                day = month = city
                break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('-' * 40)
    return city, month, day


def get_month():
    """
    prompts user for the month
    Returns: month
    """
    while True:
        month = str.lower(input("which month ? : ")).strip()
        if month in months:
            return month
        else:
            print("Sorry try again ")


def get_day():
    """
        prompts user for the day of the week
        Returns: day of the week
        """
    while True:
        day = str.lower(input("which day ? : ")).strip()
        if day in days:
            return day
        else:
            print("Sorry try again ")


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
    city = str.lower(city)
    file_path = CITY_DATA[city]
    df = pd.read_csv(file_path)

    # convert start and end time to date time type
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["Start Time"])

    # Extract month , day and hour from start time
    df["Month"] = df["Start Time"].dt.month_name(locale='English').str.lower()
    df["day"] = df["Start Time"].dt.day_name(locale='English').str.lower()
    df["hour"] = df["Start Time"].dt.hour

    if month != "all":
        if day != "all":
            return df[(df["day"] == day) & (df["Month"] == month)]
        return df[df["Month"] == month]

    if month == "all":
        if day != "all":
            return df[df["day"] == day]
        return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print(Fore.BLUE + '\nCalculating The Most Frequent Times of Travel...\n' + Style.RESET_ALL)
    start_time = time.time()

    # display the most common month
    most_common_month = df["Month"].value_counts().nlargest(1)
    print(f"Popular Month : {str.capitalize(most_common_month.index[0])} . count: {most_common_month[0]} ")

    # display the most common day of week
    most_common_day = df["day"].value_counts().nlargest(1)
    print(f"Popular Day : {str.capitalize(most_common_day.index[0])} . count : {most_common_day[0]}")

    # display the most common start hour
    most_common_hour = df["hour"].mode()
    print(f"Popular start time : {most_common_hour[0]} hrs")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print(Fore.BLUE + '\nCalculating The Most Popular Stations and Trip...\n' + Style.RESET_ALL)
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df["Start Station"].value_counts().nlargest(1)
    print(f"Start station : {most_common_start_station.index[0]} . count : {most_common_start_station[0]}")

    # display most commonly used end station
    most_common_end_station = df["End Station"].value_counts().nlargest(1)
    print(f"End Station : {most_common_end_station.index[0]} . count : {most_common_end_station[0]}")

    # display most frequent combination of start station and end station trip
    Temp = df.groupby(by=["Start Station", "End Station"]).size().sort_values(ascending=False).reset_index()
    print(Fore.MAGENTA + "Most Frequent start and end station : " + Style.RESET_ALL)
    print(f"{Temp['Start Station'][0]} <> {Temp['End Station'][0]} . count {Temp[0][0]}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print(Fore.BLUE + '\nCalculating Trip Duration...\n' + Style.RESET_ALL)
    start_time = time.time()
    # display total travel time
    print("Total travel time : ", df["Trip Duration"].sum())
    # display mean travel time
    print("Average travel time: ", df["Trip Duration"].mean())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print(Fore.BLUE + '\nCalculating User Stats...\n' + Style.RESET_ALL)
    start_time = time.time()

    # Display counts of user types
    print(Fore.MAGENTA + "User counts" + Style.RESET_ALL)
    Temp = pd.DataFrame(df["User Type"].value_counts())
    for index in Temp.index:
        print(f"{index} : {Temp.loc[index][0]}")

    # Display counts of gender
    if "Gender" in list(df.columns):
        Temp = pd.DataFrame(df["User Type"].value_counts())
        print(Fore.MAGENTA + "\nGender counts" + Style.RESET_ALL)
        for index in Temp.index:
            print(f"{index} : {Temp.loc[index][0]}")

    print("\n")
    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in list(df.columns):
        min_year = int(df["Birth Year"].min())
        max_year = int(df["Birth Year"].max())
        most_common_year = int(df["Birth Year"].mode()[0])
        print(f"Earliest YOB {min_year}")
        print(f"Recent YOB {max_year}")
        print(f"Popular YOB {most_common_year}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def get_sample(df: pd.DataFrame, start: int, end: int) -> pd.DataFrame:
    """
    Returns 5 records of the raw data..

    Args:
        df - dataframe
        (int) start - index of the first record
        (int) end - index of the last record
    Returns:
        df - Pandas DataFrame with 5 records
    """
    temp_df = df.iloc[start:end, :]
    print(temp_df)


def main():
    while True:
        city, month, day = get_filters()
        if (not city) and (not month) and (not day):
            print(Fore.RED + "Bye ! , you joking too much..am out" + Style.RESET_ALL)
            break
        print(
            Fore.BLUE + f"Current Filters for {str.capitalize(city)}, Month : {str.capitalize(month)}, Day : {str.capitalize(day)}" + Style.RESET_ALL)
        df = load_data(city, month, day)
        if len(df) > 0:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            start = 0
            end = 5
            while True:
                response = str.lower(input("Would you wish to see sample data ? ")).strip()
                if response == "yes":
                    get_sample(df, start, end)
                    start += 5
                    end += 5
                else:
                    break
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break

        print(f"No records for {city}, {month}, {day}")


if __name__ == "__main__":
    main()
