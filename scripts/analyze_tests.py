import pandas as pd

df = pd.read_csv('data/test_results.csv')
print(df.describe(include='all'))