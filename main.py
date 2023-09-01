import pandas as pd
import numpy as np

from src.utils import getSnapshotTime
from src.step1_ingest import step1_ingest
from src.step2_clean_and_output import step2_clean_and_output
from src.step3_compute_trends import step3_compute_trends

### WRAP EACH OF THE COMPONENT STEPS IN A MASTER FUNCTION ###

# def master_func():
    
# specify URL to scrape
polls_url = 'https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html'

print(f"Process started at {getSnapshotTime()}")

### ATTEMPT TO INGEST POLL DATA, PROCESS IT, AND SAVE IT ###

try:

    ### STEP 1: ATTEMPT TO INGEST, GET LATEST POLL UPDATE DATE ###
    polls, datestamp = step1_ingest(polls_url)

    ### STEP 2: CLEAN AND OUTPUT FOR CANDIDATES AVAILABLE ###
    polls, cand_names = step2_clean_and_output(polls)

### IF THOSE STEPS FAIL, READ IN PRE-SAVED CLEANED POLL DATA ###

except:
    print("Warning: polls could not be successfully ingested from page or processed. Legacy polls.csv will be read in.")
    polls = pd.read_csv('polls.csv')
    # since we won't have done this earlier, we need to extract candidate names from this newly read-in df
    cand_names = polls.columns[~polls.columns.isin(['date','pollster','n'])]
    # and the most recent datestamp will simply be the date of the most recent poll
    datestamp = polls.date.max()

### STEP 3: CREATE TRENDS FILE FROM WHATEVER PROCESSED POLLING IS AVAILABLE ###

step3_compute_trends(polls, cand_names, datestamp)

print(f"Process completed at {getSnapshotTime()}")