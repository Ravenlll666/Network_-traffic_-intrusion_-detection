import pandas as pd
import sklearn
from sklearn.preprocessing import LabelEncoder
def load_train_data():
    train_df = pd.read_csv("Dataset\\Train.csv")
    return train_df

def load_test_data():
    test_df = pd.read_csv("Dataset\\Test.csv")
    return test_df

print("Both datasets loaded successfully!!")











df= pd.read_csv("Dataset\\Train.csv")
print("data loaded successfully")

label_encoder = LabelEncoder()
label_encoder.fit(df['label'])
df['label'] = label_encoder.transform(df['label'])
