from Dataloader import load_train_data , load_test_data
import pandas as pd
import sklearn
from sklearn.preprocessing import LabelEncoder,StandardScaler ,OneHotEncoder
def preprocess_data():
    train_df = load_train_data()

    test_df = load_test_data()


    label_encoder = LabelEncoder()#label encoder
    label_encoder.fit(train_df['label'])
    train_df['label'] = label_encoder.transform(train_df['label'])#label encoding done 
            #OneHotEncoding 

    One_hot_encoding = OneHotEncoder(drop='first',sparse_output=False,handle_unknown="ignore")
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
    train_df = train_df.drop(
                columns=['flag', 'protocol_type', 'service']
            )

            # Add the encoded columns to the dataset
    train_df = pd.concat([train_df, OHE_df], axis=1)

    #print("Training data Encoding Done")

            # Test Dataset 
            
                #Lable encoding
    test_df['label'] = label_encoder.transform(test_df['label'])#label encoding done 

                #OneHotEncoding 
    test_OHE_encoding = One_hot_encoding.transform(
    test_df[['flag', 'protocol_type', 'service']]
)

    test_OHE_df = pd.DataFrame(
    test_OHE_encoding,
    columns=One_hot_encoding.get_feature_names_out(
        ['flag', 'protocol_type', 'service']
    ),
    index=test_df.index
)
    test_df = test_df.drop(columns=['flag', 'protocol_type', 'service'])



            # Add the encoded columns to the dataset
    test_df = pd.concat([test_df, test_OHE_df], axis=1)
    #print("testing data Encoding Done")
        

            #Scaler 


    x_train = train_df.drop(columns=['label'])
    y_train = train_df['label']

    x_test = test_df.drop(columns=['label'])
    y_test = test_df['label']

            #train scaler
    scaler = StandardScaler()
    scaled_xtrain = scaler.fit_transform( x_train)

            #test scaler 
    scaled_xtest = scaler.transform(x_test)
    print("all good")
    print(train_df["label"].isnull().sum())
    print(test_df["label"].isnull().sum())

    return scaled_xtrain,scaled_xtest,y_train,y_test










   









   

 