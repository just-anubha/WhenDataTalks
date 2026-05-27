import pandas as pd

df = pd.read_csv("data/bollywood.csv")
print(df[['title', 'worldwide_gross', 'year']].head(10).to_string())