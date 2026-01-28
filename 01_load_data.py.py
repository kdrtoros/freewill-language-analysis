import pandas as pd

df = pd.read_excel("freewill.xlsx")

print(df.head())
print("\nColumns:")
print(df.columns)
print("\nNumber of rows:", len(df))
