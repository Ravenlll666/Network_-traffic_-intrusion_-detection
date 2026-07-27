import pandas as pd

def load_train_data():
    train_df = pd.read_csv("Dataset\\Train.csv")
    return train_df

def load_test_data():
    test_df = pd.read_csv("Dataset\\Test.csv")
    return test_df

#print("Both datasets loaded successfully!!")












