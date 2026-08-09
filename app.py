from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

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
@app.route("/api/test")
def api_test():
    return {
        "status": "online",
        "message": "NIDS API is working"
    }
@app.route("/api/predict")
def api_predict():

    row_number = int(request.args.get("row", 0))

    test = pd.read_csv("Dataset/Test.csv")

    # Select packet
    packet = test.iloc[[row_number]]

    # -----------------------------
    # Original packet information
    # -----------------------------
    source_ip = packet["src_ip"].iloc[0] if "src_ip" in packet.columns else "N/A"
    destination_ip = packet["dst_ip"].iloc[0] if "dst_ip" in packet.columns else "N/A"
    protocol = packet["protocol_type"].iloc[0]
    service = packet["service"].iloc[0]
    tcp_flag = packet["flag"].iloc[0]

    # -----------------------------
    # Prepare packet for model
    # -----------------------------
    packet_features = packet.drop(
        columns=["label"],
        errors="ignore"
    )

    categorical_columns = [
        "flag",
        "protocol_type",
        "service"
    ]

    encoded = encoder.transform(
        packet_features[categorical_columns]
    )

    encoded_df = pd.DataFrame(
        encoded,
        columns=encoder.get_feature_names_out(
            categorical_columns
        ),
        index=packet_features.index
    )

    packet_features = packet_features.drop(
        columns=categorical_columns
    )

    packet_features = pd.concat(
        [packet_features, encoded_df],
        axis=1
    )

    # -----------------------------
    # Scale
    # -----------------------------
    scaled_packet = scaler.transform(packet_features)

    # -----------------------------
    # Prediction
    # -----------------------------
    prediction = model.predict(scaled_packet)

    attack = label_encoder.inverse_transform(
        prediction
    )[0]

    # -----------------------------
    # Confidence
    # -----------------------------
    probabilities = model.predict_proba(
        scaled_packet
    )

    confidence = float(
        probabilities.max() * 100
    )

    # -----------------------------
    # Threat level
    # -----------------------------
    if attack != "Normal":

        if confidence >= 90:
            threat = "HIGH"

        elif confidence >= 70:
            threat = "MEDIUM"

        else:
            threat = "LOW"

    else:
        threat = "SAFE"

    # -----------------------------
    # API response
    # -----------------------------
    packet_id = row_number + 1
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "packet_id": packet_id,
        "timestamp": timestamp, 
        "source_ip": str(source_ip),
        "destination_ip": str(destination_ip),
        "protocol": str(protocol).upper(),
        "service": str(service).upper(),
        "tcp_flag": str(tcp_flag).upper(),
        "prediction": str(attack),
        "confidence": round(confidence, 2),
        "threat_level": threat
    }

    
if __name__ == "__main__":
    app.run(debug=True)