import pandas as pd
import matplotlib.pyplot as plt 

df = pd.read_csv('6g.csv',skip_blank_lines=True)
print("Number of datapoints :", len(df))

# print(df.head(5))
df.columns = df.columns.str.strip()

print(df.columns.tolist())
print('Efficiency_Status' in df.columns)