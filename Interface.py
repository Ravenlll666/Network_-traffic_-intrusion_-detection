import joblib 
import pandas as pd
import random






scaler = joblib.load("model/scaler.pkl")
One_hot_encoding = joblib.load("model/encoder.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")

model = joblib.load("model/xgb_model.pkl")

test = pd.read_csv("Dataset/Test.csv")
row = int(input("Enter the row number to test: "))
packet = test.iloc[[row]]



# Save original values
protocol = packet['protocol_type'].iloc[0]
service = packet['service'].iloc[0]
flag = packet['flag'].iloc[0]
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


source_ip = f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"

destination_ip = f"10.0.{random.randint(0,255)}.{random.randint(1,254)}"
print("="*40)
print("           NETWORK IDS RESULT")
print("="*40)
print(f"Source IP     : {source_ip}")
print(f"Destination IP: {destination_ip}")
print(f"Protocol      : {protocol.upper()}")
print(f"Service       : {service.upper()}")
print(f"TCP Flag      : {flag.upper()}")

if attack[0] == "Normal":
    print(  "Prediction: Normal Traffic")
else: print(f"Prediction: {attack[0]} Attack")

print("Confidence:", f"{confidence:.1f}%" )
if attack[0] != "Normal":
  if confidence >= 90:
    threat = "HIGH"
    print(f"Threat Level  : {threat}")  

  elif confidence >=70:
    threat = "MEDIUM"
    print(f"Threat Level  : {threat}")  

  else:
    threat = "LOW"
    print(f"Threat Level  : {threat}")  

