import sys


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(r'C:\Users\danie\Documents\GitHub\ENGR315-sp2026-student\data\covid\us-counties.csv')
    except FileNotFoundError:
        print('File ', r'C:\Users\danie\Documents\GitHub\ENGR315-sp2026-student\data\covid\us-counties.csv', ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries and entries outside of Harrisonburg and Rockingham.
        if state != "Virginia":
            continue
        if county != "Harrisonburg city" and county != "Rockingham":
            continue
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

def first_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    :return:
    """

    # your code here
    #Sort the data by date and then find the first entry for each locality with cases > 0
    data.sort(key=lambda x: x[0])  # Sort by date
    rockingham_first = None
    harrisonburg_first = None

    for date, county, state, fips, cases, deaths in data:
        if county == "Rockingham" and cases > 0:
            if rockingham_first is None:
                rockingham_first = date
        if county == "Harrisonburg city" and cases > 0:
            if harrisonburg_first is None:
                harrisonburg_first = date

    print("First positive COVID case in Rockingham County:", rockingham_first)
    print("First positive COVID case in Harrisonburg:", harrisonburg_first)

    return

def second_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    :return:
    """

    # your code here
    # To find the greatest number of new daily cases, we need to calculate the daily new cases from the cumulative cases.
    data.sort(key=lambda x: (x[1], x[0]))  # Sort by county and then by date
    rockingham_cases = {}
    harrisonburg_cases = {}
    # Calculate daily new cases by taking the difference between consecutive entries for each locality
    for date, county, state, fips, cases, deaths in data:
        if county == "Rockingham":
            rockingham_cases[date] = cases
        elif county == "Harrisonburg city":
            harrisonburg_cases[date] = cases
    rockingham_new_cases = {date: rockingham_cases[date] - rockingham_cases.get(prev_date, 0) for date, prev_date in zip(sorted(rockingham_cases.keys())[1:], sorted(rockingham_cases.keys())[:-1])}
    harrisonburg_new_cases = {date: harrisonburg_cases[date] - harrisonburg_cases.get(prev_date, 0) for date, prev_date in zip(sorted(harrisonburg_cases.keys())[1:], sorted(harrisonburg_cases.keys())[:-1])}
    # Find the day with the greatest number of new daily cases for each locality
    rockingham_max_day = max(rockingham_new_cases, key=rockingham_new_cases.get)
    harrisonburg_max_day = max(harrisonburg_new_cases, key=harrisonburg_new_cases.get)
    #print both the number of new cases and the corresponding day
    print("Greatest number of new daily cases in Rockingham County:", rockingham_new_cases[rockingham_max_day], " on ", rockingham_max_day)
    print("Greatest number of new daily cases in Harrisonburg:", harrisonburg_new_cases[harrisonburg_max_day], " on ", harrisonburg_max_day)
    return

def third_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What was the worst 7-day period in either the city and county for new COVID cases?
    # This is the 7-day period where the number of new cases was maximal.
    :return:
    """
    
    # your code here
    #set up the sorting, and then calculate the daily new cases just as above, but then calculate the 7-day sums of new cases for each locality and find a maximum.
    data.sort(key=lambda x: (x[1], x[0]))  # Sort by county and then by date
    rockingham_cases = {}
    harrisonburg_cases = {}
    for date, county, state, fips, cases, deaths in data:
        if county == "Rockingham":
            rockingham_cases[date] = cases
        elif county == "Harrisonburg city":
            harrisonburg_cases[date] = cases
   # Calculate daily new cases by taking the difference between neighboring entries for each region
    rockingham_new_cases = {date: rockingham_cases[date] - rockingham_cases.get(prev_date, 0) for date, prev_date in zip(sorted(rockingham_cases.keys())[1:], sorted(rockingham_cases.keys())[:-1])}
    harrisonburg_new_cases = {date: harrisonburg_cases[date] - harrisonburg_cases.get(prev_date, 0) for date, prev_date in zip(sorted(harrisonburg_cases.keys())[1:], sorted(harrisonburg_cases.keys())[:-1])}
    
    # Calculate the 7-day sums of new cases for each region and find a maximum.
    rockingham_7day_sums = {date: sum(rockingham_new_cases.get(prev_date, 0) for prev_date in sorted(rockingham_new_cases.keys())[max(0, sorted(rockingham_new_cases.keys()).index(date)-6):sorted(rockingham_new_cases.keys()).index(date)+1]) for date in sorted(rockingham_new_cases.keys())}
    harrisonburg_7day_sums = {date: sum(harrisonburg_new_cases.get(prev_date, 0) for prev_date in sorted(harrisonburg_new_cases.keys())[max(0, sorted(harrisonburg_new_cases.keys()).index(date)-6):sorted(harrisonburg_new_cases.keys()).index(date)+1]) for date in sorted(harrisonburg_new_cases.keys())}
    
    # Find the day with the greatest number of new cases in a 7-day period for each region
    rockingham_worst_day = max(rockingham_7day_sums, key=rockingham_7day_sums.get)
    harrisonburg_worst_day = max(harrisonburg_7day_sums, key=harrisonburg_7day_sums.get)
    
    #Print out results for both regions, including both the number of cases and the day when the period ended.
    print("Worst 7-day period in Rockingham County:", rockingham_7day_sums[rockingham_worst_day], " ending on ", rockingham_worst_day)
    print("Worst 7-day period in Harrisonburg:", harrisonburg_7day_sums[harrisonburg_worst_day], " ending on ", harrisonburg_worst_day)
    return

if __name__ == "__main__":
    data = parse_nyt_data('us-counties.csv')

    for (date,county, state, fips, cases, deaths) in data:
        print('On ', date, ' in ', county, ' ', state, ' there were ', cases, ' cases and ', deaths, ' deaths')


    # write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    first_question(data)


    # write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    second_question(data)

    # write code to address the following question: Use print() to display your responses.
    # What was the worst seven day period in Harrisonburg for new COVID cases (in terms of absolute number of cases)?
    # What was the worst seven day period in Rockingham County for new COVID cases (in terms of absolute number of cases)?
    third_question(data)


