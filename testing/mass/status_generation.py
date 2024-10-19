import pandas as pd
df = pd.read_csv("files\\schools_and_districts.csv", dtype=str)
status_df = df[['code']]
status_df['status'] = 'todo'
status_df.to_csv("files\\status.csv", index=False)