import pandas as pd

missing_values = ["n/a", "na", "--"]
df = pd.read_csv('property-data.csv', na_values = missing_values)

print(df.to_string())

new_df = df.dropna()

print(new_df.to_string())

# print (df['NUM_BEDROOMS'])
# print (df['NUM_BEDROOMS'].isnull())