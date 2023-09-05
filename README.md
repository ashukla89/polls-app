# polls-app
This is a small Python app to scrape and process polls from [this page](https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html) and calculate rough trendlines from them.


## Description
This app consists of three scripts yoked together by a wrapper, `main.py`:
* Step 1 scrapes the page above and pulls the contents into a pandas dataframe
* Step 2 cleans, formats, and saves that data to a csv
* Step 3 computes and saves a running polling average from that data by running a [lowess regression](https://en.wikipedia.org/wiki/Local_regression) for available polling dates and then filling forward the smoothed regression values to dates lacking polling. Note two other choices made when handling the data:
    * For the purposes of this exercise, sample sizes, sampling methodology, and all qualifications (i.e. caveats denoted by the asterisks in the polling table) were ignored.
    * For candidates included in two polls taken on the same date, the smoothed polling values were simply averaged for that date.

## Requirements/ Setup
Python is notoriously finicky when it comes to versioning. Still, this should be lightweight enough to run from a typical Python 3.9 environment after doing a quick `pip install -r requirements.txt`, which should get you the necessary versions of pandas, numpy, statsmodels, etc.

## Running the app
This, hopefully, is the easy part. Simply run `python3 main.py` every time you'd like to run the whole shebang.