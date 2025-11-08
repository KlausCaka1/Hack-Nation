import pandas as pd

# Load the dataset
jobs_df = pd.read_csv(r"C:\Users\klaus\Documents\postings.csv")

jobs_df.to_json("job-descriptions.json", orient="records", lines=True)
