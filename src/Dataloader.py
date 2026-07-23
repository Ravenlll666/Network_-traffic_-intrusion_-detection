import pandas as pd


df= pd.read_csv("Dataset\\Train.csv")
print("data loaded successfully")

print(df.duplicated().sum())