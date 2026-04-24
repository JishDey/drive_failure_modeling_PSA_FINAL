# Modeling Hard Drive Failures

## Notes
All files are run through a local venv shebang, but the shebang line for venv
could be incorrect based on your operating system. 
(e.g. both `python3 ./stack_tables.py` or `./stack_tables.py` are valid)

The main project folder, which holds the `model_failures.py` shall be called
the 'main folder'.

## Full Run Instructions

Start a venv environment.

Run `pip install pandas scipy numpy matplotlib`.

For our final results, we used 3 years of data from the [backblaze website](https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data#downloadingTheRawTestData).
Download and unzip Q1-4 for each year. Keep each day's record in it's quarter
folder. Put each quarter folder in a folder called `data`, in the main folder.

Make a folder called `merged_quarters`.

Run `stack_quarter.py` on each folder - merged_quarters should add a `.csv` file
for each quarter. When you have compressed all of your folders, you can move on.
(Alternatively, if the dataset is too big, you can compress each folder, delete
it, and then download the next one)

Run `stack_tables.py`. You should see lifetime_data.csv in the main directory.

Run `model_failures.py`. The results will be printed in the terminal, as well as
displayed via matplotlib.