import pandas as pd

df = pd.read_json('anime_data.json')

print(df.head(10))