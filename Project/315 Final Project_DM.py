import sys
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def parse_healthcare_data(file_path=''):
    # Read the healthcare data from the specified file path and return it as list of tuples.
    # Each tuple contains:
    # (year, location, question, data_value)

    # create a list to hold the raw data
    data = []

    # dictionary to accumulate totals and counts per year, question, and state
    # structure: {year: {question: {state: [sum, count]}}}
    year_question_state_data = {}

   
    filepath = file_path

    # open the csv file path
    try:
        fin = open(filepath, newline='')
    except FileNotFoundError:
        print('File ', filepath, ' not found. Exiting!')
        sys.exit(-1)

    # use csv dictionary reader so we can access columns by name
    reader = csv.DictReader(fin)

    # loop and read file
    for row in reader:

        # ensure required columns exist in the row
        try:
            YearStart = int(row['YearStart'])
            LocationAbbr = row['LocationAbbr']
            Question = row['Question']
            Data_Value = float(row['Data_Value'])
        except (KeyError, ValueError):
            continue

        # print raw parsed record (as requested)
        print(YearStart, LocationAbbr, Question, Data_Value)

        # store raw entry
        entry = (YearStart, LocationAbbr, Question, Data_Value)
        data.append(entry)

        # accumulate sum and count per year, question, and state

        # initialize year if needed
        if YearStart not in year_question_state_data:
            year_question_state_data[YearStart] = {}

        # initialize question if needed
        if Question not in year_question_state_data[YearStart]:
            year_question_state_data[YearStart][Question] = {}

        # initialize state if needed
        if LocationAbbr not in year_question_state_data[YearStart][Question]:
            year_question_state_data[YearStart][Question][LocationAbbr] = [0.0, 0]

        # update sum and count
        year_question_state_data[YearStart][Question][LocationAbbr][0] += Data_Value
        year_question_state_data[YearStart][Question][LocationAbbr][1] += 1

    fin.close()

    # calculate averages per year, question, and state

    year_question_state_averages = {}

    for year in year_question_state_data:
        year_question_state_averages[year] = {}

        for question in year_question_state_data[year]:
            year_question_state_averages[year][question] = {}

            for state in year_question_state_data[year][question]:

                total, count = year_question_state_data[year][question][state]
                avg = total / count

                year_question_state_averages[year][question][state] = avg

    # print averages for verification

    print("\nAverages by Year, Question, and State:\n")

    for year in year_question_state_averages:
        for question in year_question_state_averages[year]:
            for state in year_question_state_averages[year][question]:

                avg = year_question_state_averages[year][question][state]

                print(year, state, question, avg)

    return year_question_state_averages

def build_analysis_table(year_question_state_averages):
    # Convert nested dictionary into a flat analysis table:
    # (year, state) → questions as columns

    rows = []

    for year in year_question_state_averages:
        for question in year_question_state_averages[year]:
            for state in year_question_state_averages[year][question]:

                value = year_question_state_averages[year][question][state]
                rows.append([year, state, question, value])

    df = pd.DataFrame(rows, columns=["Year", "State", "Question", "Value"])

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
    INACTIVITY_Q = "Percent of adults who engage in no leisure-time physical activity"
    FRUIT_Q = "Percent of adults who report consuming fruit less than one time daily"

    # clean dataset
    df = pivot_df[["Year", OBESITY_Q, INACTIVITY_Q, FRUIT_Q]].dropna()

    years = sorted(df["Year"].unique())

    # -----------------------------
    # OBESITY vs INACTIVITY
    # -----------------------------
    plt.figure()

    print("\nCorrelation: Obesity vs Physical Inactivity (by year)")

    for year in years:

        subset = df[df["Year"] == year]

        x = subset[INACTIVITY_Q]
        y = subset[OBESITY_Q]

        # correlation coefficient (skip if not enough data)
        if len(subset) > 1:
            corr = np.corrcoef(x, y)[0, 1]
        else:
            corr = np.nan

        print(f"{year}: r = {corr}")

        # scatter
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
    plt.show()

    # -----------------------------
    # OBESITY vs FRUIT CONSUMPTION
    # -----------------------------
    plt.figure()

    print("\nCorrelation: Obesity vs Fruit Consumption (by year)")

    for year in years:

        subset = df[df["Year"] == year]

        x = subset[FRUIT_Q]
        y = subset[OBESITY_Q]

        if len(subset) > 1:
            corr = np.corrcoef(x, y)[0, 1]
        else:
            corr = np.nan

        print(f"{year}: r = {corr}")

        plt.scatter(x, y, label=f"{year} (r={corr:.2f})")

        if len(subset) > 1:
            m, b = np.polyfit(x, y, 1)
            trend = m * x + b
            plt.plot(x, trend)

    plt.xlabel("Low Fruit Consumption")
    plt.ylabel("Obesity Rate")
    plt.title("Obesity vs Dietary Habits (by Year)")
    plt.legend()
    plt.show()


# run parser
year_question_state_averages = parse_healthcare_data(r"C:\Users\danie\Documents\GitHub\ENGR315-sp2026-student\Project\315 Project Nutrition Data.csv")

# build analysis table
pivot_df = build_analysis_table(year_question_state_averages)

# run analysis
analyze_relationships_by_year(pivot_df)




