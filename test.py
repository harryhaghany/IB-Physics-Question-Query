import pandas as pd

df = pd.read_csv('Output.csv', delimiter=';')

print(df.to_string()) 