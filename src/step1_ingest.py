import pandas as pd
import numpy as np

from datetime import datetime

from src.utils import getSnapshotTime

import requests
from bs4 import BeautifulSoup

### DEFINE HELPER FUNCTIONS AS NEEDED ###

# function to check and get response
def get_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Response successful at {getSnapshotTime()}: status code 200")
        return response
    else:
        print(f"Error: Response unsuccessful at {getSnapshotTime()}: status code {response.status_code}")
        
# function to check for and store valid timestamp
def get_datestamp(doc):
    if doc.find('h1') is not None:
        datestamp = datetime.strptime(doc.find('h1').text.replace("Poll data as of ",""), "%B %d, %Y")
        print(f"Data pulled for page updated as of {datestamp}")
        return datestamp
    else:
        print("Warning: page date not found.")
        
### DEFINE INGESTION PROCESS AS SINGLE FUNCTION ###

def step1_ingest(polls_url):

    # read in page HTML
    response = get_response(polls_url)
    
    print(response.text)

    # convert text to bs4 object
    try:
        doc = BeautifulSoup(response.text, features="html5lib")
    except:
        print("Error: content of polls page could not be read")

    # extract most recent update date, for error-handling purposes
    datestamp = get_datestamp(doc)

    # extract table of election results, throw error if no table found
    try:
        table = doc.find("table")
        print(f"Table successfully extracted at {getSnapshotTime()}")
    except:
        print("Error: Table on polls page could not be found")

    # extract column names from table headers
    try:
        cols = [head.text.strip() for head in table.find('thead').find_all('th')]
        print(f"Column headers successfully read in at {getSnapshotTime()}")
    except:
        print("Error: valid table headers could not be found")

    # extract asterisk values
    """
        Note that we're not doing anything with these for now.
        Qualifiers on sampling methodology or decisions to include certain candidates may be relevant later,
        but for this exercise we're computing a simple sample-agnostic lowess average (see step 3).
    """
    
    try:
        ul = doc.find("ul")
        ast_rows = []
        for li in ul.find_all("li"):
            row = {}
            row['symbol'] = li['data-mark']
            row['definition'] = li.text.strip()
            ast_rows.append(row)

        asts = pd.DataFrame(ast_rows)
        print(f"Qualifications/ asterisks read in at {getSnapshotTime()}")
    except:
        print("Note: No qualifying notes for any polls were found")

    # instantiate rows list for iterating through table
    rows = []

    # iterate through rows of the table body
    try:
        for tr in table.find('tbody').find_all('tr'):
            # capture each data point in that row
            data = tr.find_all('td')
            # instantiate row dict to label per column names
            row = {}
            # iterate through length of cols list, assuming no datum is in the wrong column
            for i in range(len(cols)):
                # label each element of the row dict per the column names, and assign the according value
                # also, strip asterisks and percent sign
                row[cols[i]] = data[i].text.strip().replace("%","").replace("*","")
            # append the row the list of rows
            rows.append(row)
    except:
        print("Error: no valid rows were found in the table of polls")

    # turn into a python df
    polls = pd.DataFrame(rows)
    
    print(f"Raw poll df generated at {getSnapshotTime()}; {len(polls)} polls found")
    
    # return polls and datestamp, both of which will be used later
    return polls, datestamp