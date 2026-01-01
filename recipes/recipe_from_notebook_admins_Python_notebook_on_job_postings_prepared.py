# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE_MAGIC_CELL
# Automatically replaced inline charts by "no-op" charts
# %pylab inline
import matplotlib
matplotlib.use("Agg")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
import dataiku
from dataiku import pandasutils as pdu
import pandas as pd

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read the dataset as a Pandas dataframe in memory
# Note: here, we only read the first 100K rows. Other sampling options are available
dataset_job_postings_prepared = dataiku.Dataset("job_postings_prepared")
df = dataset_job_postings_prepared.get_dataframe(limit=100000)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Define a function to extract the minimum salary
def extract_min_salary(salary_range):
    if pd.isna(salary_range):  # Keep missing values as missing
        return None
    try:
        min_salary = int(salary_range.split('-')[0])  # Extract minimum salary
        return min_salary
    except:
        return None  # Handle invalid values

# Apply the function and convert to integer type
df['min_salary'] = df['salary_range'].apply(extract_min_salary).astype('Int64')

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Recipe outputs
job_postings_python = dataiku.Dataset("job_postings_python")
job_postings_python.write_with_schema(df)