import sys
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# FILE PATH PLACEHOLDER
# ============================================================

# replace this placeholder with your own file path
FILE_PATH = r"Project\315 Project Nutrition Data.csv"


# ============================================================
# PARSING FUNCTION
# ============================================================

def parse_healthcare_data(file_path=''):
    # Read the healthcare data from the specified file path.
    # This function creates several storage structures that are used
    # by the different analysis functions below.

    # STORAGE STRUCTURES

    raw_data = []
    # stores raw data as tuples:
    # (year, state, question, demographic, data_value)

    year_question_state_data = {}
    # dictionary to accumulate totals and counts per year, question, and state
    # structure: {year: {question: {state: [sum, count]}}}

    obesity_demographic_data = {}
    # stores obesity data by question + demographic
    # structure: {question: {demographic: [sum, count]}}

    # OPEN FILE

    filepath = file_path

    try:
        fin = open(filepath, newline='', encoding='utf-8')
    except FileNotFoundError:
        print('File', filepath, 'not found. Exiting!')
        sys.exit(-1)

    # use csv dictionary reader so we can access columns by name
    reader = csv.DictReader(fin)

    # READ DATA

    # loop through each row and extract only the relevant columns
    for row in reader:

        # ensure required columns exist in the row
        try:
            year = int(row['YearStart'])
            state = row['LocationAbbr']
            question = row['Question']
            demographic = row['Stratification1']
            data_value = float(row['Data_Value'])

        except (KeyError, ValueError):
            continue  # skip bad rows or empty data values

        # skip empty demographics
        if demographic.strip() == '':
            continue

        # STORE RAW ENTRY

        entry = (year, state, question, demographic, data_value)

        # append the data as a tuple to the list
        raw_data.append(entry)

        # BUILD YEAR / QUESTION / STATE DATA STRUCTURE

        # initialize year if needed
        if year not in year_question_state_data:
            year_question_state_data[year] = {}

        # initialize question if needed
        if question not in year_question_state_data[year]:
            year_question_state_data[year][question] = {}

        # initialize state if needed
        if state not in year_question_state_data[year][question]:
            year_question_state_data[year][question][state] = [0.0, 0]
            # [sum, count]

        # add value
        year_question_state_data[year][question][state][0] += data_value

        # increment count
        year_question_state_data[year][question][state][1] += 1

        # BUILD OBESITY / DEMOGRAPHIC DATA STRUCTURE

        # only keep obesity-related questions
        if 'obesity' in question.lower():

            if question not in obesity_demographic_data:
                obesity_demographic_data[question] = {}

            if demographic not in obesity_demographic_data[question]:
                obesity_demographic_data[question][demographic] = [0.0, 0]
                # [sum, count]

            # add obesity value
            obesity_demographic_data[question][demographic][0] += data_value

            # increment count
            obesity_demographic_data[question][demographic][1] += 1

    # close file
    fin.close()

    # CALCULATE AVERAGES BY YEAR, QUESTION, AND STATE

    year_question_state_averages = {}

    for year in year_question_state_data:

        year_question_state_averages[year] = {}

        for question in year_question_state_data[year]:

            year_question_state_averages[year][question] = {}

            for state in year_question_state_data[year][question]:

                total, count = year_question_state_data[year][question][state]

                # compute average value
                avg = total / count

                year_question_state_averages[year][question][state] = avg

    # CALCULATE AVERAGE OBESITY RATES BY DEMOGRAPHIC

    obesity_demographic_averages = {}

    for question in obesity_demographic_data:

        obesity_demographic_averages[question] = {}

        for demographic in obesity_demographic_data[question]:

            total, count = obesity_demographic_data[question][demographic]

            # compute average obesity rate
            obesity_demographic_averages[question][demographic] = total / count

    # return both analysis structures
    return raw_data, year_question_state_averages, obesity_demographic_averages


# ============================================================
# ANALYSIS 1: OBESITY BY DEMOGRAPHIC GROUP
# ============================================================

def analyze_obesity_by_demographic(obesity_demographic_averages):

    # TERMINAL OUTPUT

    print("\nAverage Obesity Rates by Demographic Group\n")

    for question in obesity_demographic_averages:

        print("\nQUESTION:", question)

        for demographic in obesity_demographic_averages[question]:

            avg = obesity_demographic_averages[question][demographic]

            print(
                "Demographic:",
                demographic,
                "| Average Obesity Rate:",
                round(avg, 2)
            )

    # CREATE DATAFRAME

    rows = []

    for question in obesity_demographic_averages:

        for demographic in obesity_demographic_averages[question]:

            rows.append({
                'Question': question,
                'Demographic': demographic,
                'Average_Obesity_Rate':
                    obesity_demographic_averages[question][demographic]
            })

    # convert rows into dataframe
    df = pd.DataFrame(rows)

    # DEMOGRAPHIC GROUP DEFINITIONS

    demographic_categories = {
        'Income': ['income', '$'],

        'Education': [
            'less than high school',
            'high school',
            'college',
            'graduate'
        ],

        'Age': ['years'],

        'Gender': ['male', 'female'],

        'Race/Ethnicity': [
            'white',
            'black',
            'hispanic',
            'asian',
            'multiracial'
        ]
    }

    # CREATE ONE GRAPH FOR EACH DEMOGRAPHIC TYPE

    for category_name, keywords in demographic_categories.items():

        category_rows = []

        # loop through dataframe rows
        for _, row in df.iterrows():

            demographic = row['Demographic'].lower()

            # check if demographic matches category
            if any(keyword in demographic for keyword in keywords):

                category_rows.append(row)

        # skip empty categories
        if len(category_rows) == 0:
            continue

        # convert to dataframe
        category_df = pd.DataFrame(category_rows)

        # compute average obesity rate
        grouped = (
            category_df.groupby('Demographic')['Average_Obesity_Rate']
            .mean()
            .sort_values(ascending=False)
        )

        # CREATE GRAPH

        plt.figure(figsize=(12, 6))

        grouped.plot(kind='bar')

        plt.title(f'Average Obesity Rate by {category_name}')

        plt.xlabel(category_name)
        plt.ylabel('Average Obesity Rate')

        # rotate labels for readability
        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()

        plt.show()


# ============================================================
# ANALYSIS 2: OBESITY RATES OVER TIME
# ============================================================

def analyze_obesity_over_time(raw_data):
    # How have obesity rates changed over time across the United States?

    # create a list to hold years the study covers for later plotting
    years = []

    # create a dictionary to hold the average obesity rates for each year
    year_averages = {}

    # define the target question we want to analyze
    target_question = 'Percent of adults aged 18 years and older who have obesity'

    # loop through the data and extract the relevant entries for the target question
    for entry in raw_data:

        year = entry[0]
        question = entry[2]
        data_value = entry[4]

        # check if the question matches the target question
        if question == target_question:

            # add the year to the list of years
            years.append(year)

            # add the data value to the list of obesity rates for that year
            if year not in year_averages:
                year_averages[year] = []

            year_averages[year].append(data_value)

    # calculate the average obesity rate for each year
    for year in year_averages:

        year_averages[year] = np.mean(year_averages[year])

    # convert the list of years to a sorted list for plotting
    years = sorted(set(years))

    # create a list of average obesity rates corresponding to the sorted years
    averages = [year_averages[year] for year in years]

    # calculate the linear correlation coefficient between years and average obesity rates
    correlation_coefficient = np.corrcoef(years, averages)[0, 1]

    # create a line of best fit for the data
    coefficients = np.polyfit(years, averages, 1)

    polynomial = np.poly1d(coefficients)

    trendline = polynomial(years)

    # PLOT RESULTS

    plt.figure(figsize=(10, 6))

    # plot average obesity rates
    plt.plot(years, averages, marker='o')

    # include the line of best fit in the plot
    plt.plot(years, trendline, 'r--', linewidth=2)

    # display the slope of the line of best fit in the plot legend
    plt.legend([
        'Average Obesity Rate',
        f'Trendline (slope: {coefficients[0]:.2f})'
    ])

    # include the correlation coefficient in the plot title
    plt.title(
        f'Average Obesity Rates in the US Over Time '
        f'(Correlation: {correlation_coefficient:.2f})'
    )

    plt.xlabel('Year')
    plt.ylabel('Average Obesity Rate (%)')
    plt.grid()
    plt.tight_layout()
    plt.show()

    # display the average obesity rate for each year
    for year in years:

        print(
            f'Year: {year}, '
            f'Average Obesity Rate: {year_averages[year]:.2f}%'
        )

    # return the years and averages for potential further analysis and the plot
    return years, averages


# ============================================================
# ANALYSIS 3: RELATIONSHIPS BETWEEN VARIABLES BY YEAR
# ============================================================

def build_analysis_table(year_question_state_averages):
    # Convert nested dictionary into a flat analysis table:
    # (year, state) → questions as columns

    rows = []

    for year in year_question_state_averages:

        for question in year_question_state_averages[year]:

            for state in year_question_state_averages[year][question]:

                value = year_question_state_averages[year][question][state]

                rows.append([year, state, question, value])

    df = pd.DataFrame(
        rows,
        columns=["Year", "State", "Question", "Value"]
    )

    # pivot into wide format for analysis
    pivot_df = df.pivot_table(
        index=["Year", "State"],
        columns="Question",
        values="Value"
    ).reset_index()

    return pivot_df


def analyze_relationships_by_year(pivot_df):

    # -------------------------------------------------
    # EDIT THESE TO MATCH YOUR DATASET EXACTLY
    # -------------------------------------------------

    OBESITY_Q = "Percent of adults aged 18 years and older who have obesity"

    INACTIVITY_Q = (
        "Percent of adults who engage in no leisure-time physical activity"
    )

    FRUIT_Q = (
        "Percent of adults who report consuming fruit less than one time daily"
    )

    # clean dataset
    df = pivot_df[
        ["Year", OBESITY_Q, INACTIVITY_Q, FRUIT_Q]
    ].dropna()

    # collect sorted years for plotting
    years = sorted(df["Year"].unique())

    # -----------------------------
    # OBESITY vs INACTIVITY
    # -----------------------------

    plt.figure(figsize=(10, 6))

    print("\nCorrelation: Obesity vs Physical Inactivity (by year)")

    for year in years:

        subset = df[df["Year"] == year]

        x = subset[INACTIVITY_Q]
        y = subset[OBESITY_Q]

        # correlation coefficient
        # skip if not enough data
        if len(subset) > 1:
            corr = np.corrcoef(x, y)[0, 1]
        else:
            corr = np.nan

        print(f"{year}: r = {corr}")

        # scatter plot
        plt.scatter(x, y, label=f"{year} (r={corr:.2f})")

        # trendline
        if len(subset) > 1:
            m, b = np.polyfit(x, y, 1)
            trend = m * x + b
            plt.plot(x, trend)

    plt.xlabel("Physical Inactivity")
    plt.ylabel("Obesity Rate")
    plt.title("Obesity vs Physical Inactivity (by Year)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

    # -----------------------------
    # OBESITY vs FRUIT CONSUMPTION
    # -----------------------------

    plt.figure(figsize=(10, 6))

    print("\nCorrelation: Obesity vs Fruit Consumption (by year)")

    for year in years:

        subset = df[df["Year"] == year]

        x = subset[FRUIT_Q]
        y = subset[OBESITY_Q]

        # correlation coefficient
        # skip if not enough data
        if len(subset) > 1:
            corr = np.corrcoef(x, y)[0, 1]
        else:
            corr = np.nan

        print(f"{year}: r = {corr}")

        # scatter plot
        plt.scatter(x, y, label=f"{year} (r={corr:.2f})")

        # trendline
        if len(subset) > 1:
            m, b = np.polyfit(x, y, 1)
            trend = m * x + b
            plt.plot(x, trend)

    plt.xlabel("Low Fruit Consumption")
    plt.ylabel("Obesity Rate")
    plt.title("Obesity vs Dietary Habits (by Year)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    # run parser
    raw_data, year_question_state_averages, obesity_demographic_averages = (
        parse_healthcare_data(FILE_PATH)
    )

    # run analysis 1
    analyze_obesity_by_demographic(obesity_demographic_averages)

    # run analysis 2
    analyze_obesity_over_time(raw_data)

    # build analysis table
    pivot_df = build_analysis_table(year_question_state_averages)

    # run analysis 3
    analyze_relationships_by_year(pivot_df)


# call main function so output actually appears
main()