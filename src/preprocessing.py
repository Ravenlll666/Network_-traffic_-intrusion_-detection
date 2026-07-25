from Dataloader import load_train_data , load_test_data
import pandas as pd
import sklearn
from sklearn.preprocessing import LabelEncoder
train_df = load_train_data()
test_df = load_test_data()


label_encoder = LabelEncoder()#label encoder
label_encoder.fit(train_df['label'])
train_df['label'] = label_encoder.transform(train_df['label'])#label encoding done 

#OneHotEncoding 
from sklearn.preprocessing import OneHotEncoder
One_hot_encoding = OneHotEncoder(drop='first',sparse_output=False)
One_hot_encoding.fit(train_df[['flag','protocol_type','service']])
OHE_encoding = One_hot_encoding.transform (train_df[['flag','protocol_type','service']])

OHE_df = pd.DataFrame(
    OHE_encoding,
    columns=One_hot_encoding.get_feature_names_out(
        ['flag', 'protocol_type', 'service']
    ),
    index=train_df.index
)

# Remove the original categorical columns
df = train_df.drop(
    columns=['flag', 'protocol_type', 'service']
)

# Add the encoded columns to the dataset
df = pd.concat([train_df, OHE_df], axis=1)

print("Training data Encoding Done")

# Test Dataset 
 
    #Lable encoding
label_encoder = LabelEncoder()#label encoder
label_encoder.fit(test_df['label'])
test_df['label'] = label_encoder.transform(test_df['label'])#label encoding done 

    #OneHotEncoding 
from sklearn.preprocessing import OneHotEncoder
test_One_hot_encoding = OneHotEncoder(drop='first',sparse_output=False)
test_One_hot_encoding.fit(test_df[['flag','protocol_type','service']])
test_OHE_encoding = test_One_hot_encoding.transform (test_df[['flag','protocol_type','service']])

test_OHE_df = pd.DataFrame(
    test_OHE_encoding,
    columns=test_One_hot_encoding.get_feature_names_out(
        ['flag', 'protocol_type', 'service']
    ),
    index=test_df.index
)

# Remove the original categorical columns
df = test_df.drop(
    columns=['flag', 'protocol_type', 'service']
)

# Add the encoded columns to the dataset
df = pd.concat([test_df, OHE_df], axis=1)

print("testing data Encoding Done")







   

 