from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model # type: ignore
import joblib  # For loading the scaler
from sklearn.preprocessing import StandardScaler

# Initialize Flask app
app = Flask(__name__)

# Load trained model
model = load_model("diabetes_model_1.h5")

scaler = joblib.load("scaler.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json()

        # Convert JSON into numpy array
        input_data = np.array([
            [
                data["Pregnancies"],
                data["Glucose"],
                data["BloodPressure"],
                data["SkinThickness"],
                data["Insulin"],
                data["BMI"],
                data["DiabetesPedigreeFunction"],
                data["Age"],
            ]
        ])

        # Scale the input data
        #scaler = StandardScaler()
        input_data_scaled = scaler.transform(input_data)

        # Get prediction (Probability)
        loaded_model = tf.keras.models.load_model("diabetes_model.h5")
        prediction = loaded_model.predict(input_data_scaled)
        print(prediction)

        # Convert probability to binary class (0 or 1)
        predicted_class = int(prediction[0][0] > 0.5)

        # Prepare response
        result = {
            "prediction": "Diabetes" if predicted_class == 1 else "No Diabetes",
            "probability": float(prediction[0][0])
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)