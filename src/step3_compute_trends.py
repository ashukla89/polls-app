import pandas as pd
import numpy as np

from datetime import datetime
from statsmodels.nonparametric.smoothers_lowess import lowess

from src.utils import getSnapshotTime

### DEFINE FUNCTION THAT WILL CONVERT POLLS INTO TRENDS USING LOWESS METHOD (MORE OR LESS) ###

def step3_compute_trends(polls, cand_names, datestamp):
    
    # instantiate a list object that will hold each candidate's smoothed data
    smoothed_data = []

    for candidate in cand_names:
        
        # Remove missing data for the candidate and set index to the date value
        candidate_data = polls[['date', candidate]].dropna()
        dates = candidate_data['date'] # get a list of the unique dates that candidate has polls for

        # save candidate-specific data
        percentages = candidate_data[candidate]

        # Apply Lowess regression considering only past dates, smoothing over 30% of available data
        smoothed = lowess(percentages, np.arange(len(dates)), frac=0.3)

        # create Series with date as index and smoothed percentages as values
        smoothed_series = pd.DataFrame(smoothed,index=dates)[1]
        smoothed_series.name = candidate # name the column after the candidate
        # aggregate by unique date
        smoothed_series = smoothed_series.groupby(level=0).mean()
        # append series to smoothed_data
        smoothed_data.append(smoothed_series)

    # Create a new DataFrame out of the smoothed data
    smoothed_df = pd.concat(smoothed_data,axis=1)

    # Generate a date range covering the entire period
    date_range = pd.date_range(start=polls.date.min(),end=datestamp,freq='D')

    # Reindex the smoothed_df to include all calendar dates and fill forward any dates without smoothed values
    smoothed_df = smoothed_df.reindex(date_range).ffill()
    # And then convert date back into a main column
    smoothed_df = smoothed_df.reset_index().rename(columns={'index':'date'})

    # write the smoothed df to trends.csv
    smoothed_df.to_csv('outputs/trends.csv')
    
    print(f"Trends dataframe generated and written to csv at {getSnapshotTime()}")