import pandas as pd
import pandasql as ps

filepath = "products.csv"
df = pd.read_csv(filepath)

print("Dataframe columns types:")
print(df.dtypes)

print("\nData of products:")
print(df)

query = "SELECT * FROM df WHERE price > 50"
result = ps.sqldf(query, globals())

print("\nQuery Result:")
print(result)
