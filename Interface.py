import joblib 
import pandas as pd




scaler = joblib.load("model/scaler.pkl")
One_hot_encoding = joblib.load("model/encoder.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")

model = joblib.load("model/xgb_model.pkl")
print("Model Loaded Successfully")
test = pd.read_csv("Dataset\\Test.csv")
packet = test.iloc[[5]]
categorical = packet[['flag', 'protocol_type', 'service']]

encoded = One_hot_encoding.transform(categorical)
encoded_df = pd.DataFrame(
    encoded,
    columns=One_hot_encoding.get_feature_names_out(
        ['flag', 'protocol_type', 'service']
    ),
    index=packet.index
)
packet = packet.drop(
    columns=['flag', 'protocol_type', 'service']
)
packet = pd.concat(
    [packet, encoded_df],
    axis=1
)
packet = packet.drop(columns=['label'])
scale_packet = scaler.transform(packet)

prediction = model.predict(scale_packet)
attack = label_encoder.inverse_transform(prediction)
probability = model.predict_proba(packet)

confidence = probability.max()*100
print("="*40)
print("           NETWORK IDS RESULT")
print("="*40)

if attack[0] == "Normal":
    print("Prediction: Normal Traffic")
else: print("Prediction:", attack[0], "Attack")

print("Confidence:", f"{confidence:.1f}%" )
