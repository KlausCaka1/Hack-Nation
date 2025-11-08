import pandas as pd

# Load the dataset
jobs_df = pd.read_csv("Pleas enter your path for the dataset you want to use")
# save dataset as json
jobs_df.to_json("job-descriptions.json", orient="records", lines=True)
