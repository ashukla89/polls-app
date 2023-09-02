import pandas as pd
import numpy as np

from datetime import datetime
import math

from src.utils import getSnapshotTime

### DEFINE HELPER FUNCTIONS TO CHECK DATA QUALITY ###

# Write function to ensure that all polls are scaled to the same magnitude (in case some are provided as decimals)
def scale_correctly(row, index, candidates):
    # if order of magnitude is 0, keep it that way
    if math.log10(round(row[candidates].sum(), -2)) == 0:
        return row
    # if order of magnitude is 2, divide by 100
    elif math.log10(round(row[candidates].sum(), -2)) == 2:
        row[candidates] = row[candidates] / 100
        return row
    # otherwise throw error: we shouldn't see any polls in other formats
    else:
        print(f"Row {index}: Poll totals on {row['date']} by {row['pollster']} have unexpected scale; poll omitted")
        return False
    
# At the appropriate scale, ensure that the poll responses sum to close to 100. Omit those that don't.
def check_for_correct_sum(row, index, candidates):
    if round(row[candidates].sum(), 2) < 0.99 or round(row[candidates].sum(), 2) > 1.01:
        # write message omitting this row
        print(f"Row {index}: Poll totals on {row['date']} by {row['pollster']} add up to {row[candidates].sum()*100}%; poll omitted")
        return False
    else:
        return True

### DEFINE FUNCTION TO CLEAN DATA AND WRITE POLLS TO CSV ###

def step2_clean_and_output(polls):
    
    # rename 'Date', 'Pollster', and 'Sample' to 'date', 'pollster', and 'n' respectively
    rename = {
        'Date':'date',
        'Pollster':'pollster',
        'Sample':'n'
    }
    try:
        polls = polls.rename(columns=rename)
        print(f"Column names successfully harmonized at {getSnapshotTime()}")
    except:
        print("Error: Non-candidate column names not as expected")
    
    # ensure date is date format
    try:
        polls['date'] = pd.to_datetime(polls['date']).dt.date
        print(f"Poll dates successfully converted to datetime format at {getSnapshotTime()}")
    except:
        print("Error: At least some poll dates found unable to be converted to datetime")

    # sort in increasing chronological order
    polls = polls.sort_values(by='date').reset_index(drop=True)
    
    # ensure numeric columns are in fact numeric
    try:
        polls.loc[:, ~polls.columns.isin(['date','pollster'])] = polls.loc[:, ~polls.columns.isin(['date','pollster'])].\
            apply(lambda x: x.str.replace(",","")).replace("",None).astype(float)
        print(f"Sample and poll values successfully converted to numeric at {getSnapshotTime()}")
    except:
        print("Error: Some sample and/ or poll values found unable to be converted to numeric")
        
    print(polls.head())
    print(polls.dtypes)

    # ensure candidate polling totals are scaled to the correct order of magnitude
    cand_names = polls.columns[~polls.columns.isin(['date','pollster','n'])]
    polls = polls.apply(lambda row: scale_correctly(row,row.name,cand_names), axis=1)

    # filter out polls that don't sum to close to 100% and print the ones that don't
    polls = polls[polls.apply(lambda row: check_for_correct_sum(row,row.name,cand_names), axis=1)]

    # write to csv
    polls.to_csv('outputs/polls.csv')

    print(f"Cleaned poll dataframe containing {len(polls)} polls generated and written to csv at {getSnapshotTime()}")

    # return running polls df, as well as the cand_names list, which we'll need later
    return polls, cand_names