import pandas as pd
import sklearn
from sklearn.preprocessing import LabelEncoder



df= pd.read_csv("Dataset\\Train.csv")
print("data loaded successfully")

label_encoder = LabelEncoder()
label_encoder.fit(df['label'])
df['label'] = label_encoder.transform(df['label'])
