from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained ML components
model = joblib.load("model/xgb_model.pkl")
scaler = joblib.load("model/scaler.pkl")
encoder = joblib.load("model/encoder.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    # Get row number from the form
    row_number = int(request.form["row_number"])

    # Load test dataset
    test = pd.read_csv("Dataset/Test.csv")

    # Select packet
    packet = test.iloc[[row_number]]

    # Keep original information for displaying
    source_ip = packet["src_ip"].iloc[0] if "src_ip" in packet.columns else "N/A"
    destination_ip = packet["dst_ip"].iloc[0] if "dst_ip" in packet.columns else "N/A"
    protocol = packet["protocol_type"].iloc[0]
    service = packet["service"].iloc[0]
    tcp_flag = packet["flag"].iloc[0]

    # Remove label if present
    packet_features = packet.drop(columns=["label"], errors="ignore")

    # One-hot encode categorical columns
    categorical_columns = ["flag", "protocol_type", "service"]

    encoded = encoder.transform(packet_features[categorical_columns])

    encoded_df = pd.DataFrame(
        encoded,
        columns=encoder.get_feature_names_out(categorical_columns),
        index=packet_features.index
    )

    # Remove original categorical columns
    packet_features = packet_features.drop(columns=categorical_columns)

    # Combine numerical + encoded features
    packet_features = pd.concat(
        [packet_features, encoded_df],
        axis=1
    )

    # Scale
    scaled_packet = scaler.transform(packet_features)

    # Prediction
    prediction = model.predict(scaled_packet)

    # Convert prediction number to attack name
    attack = label_encoder.inverse_transform(prediction)[0]

    # Confidence
    probabilities = model.predict_proba(scaled_packet)
    confidence = probabilities.max() * 100

    # Threat level
    if attack != "Normal":

        if confidence >= 90:
            threat = "HIGH"
        elif confidence >= 70:
            threat = "MEDIUM"
        else:
            threat = "LOW"

    else:
        threat = "SAFE"

    return render_template(
        "result.html",
        source_ip=source_ip,
        destination_ip=destination_ip,
        protocol=protocol,
        service=service,
        tcp_flag=tcp_flag,
        attack=attack,
        confidence=round(confidence, 2),
        threat=threat
    )


if __name__ == "__main__":
    app.run(debug=True)