import streamlit as st
import requests
import json

# Flask API endpoint
FLASK_API_URL = "http://127.0.0.1:5000/predict"

# Streamlit UI
st.title("🩺 Diabetes Prediction App")
st.write("Enter the patient's details and click 'Predict' to check the risk of diabetes.")

# Create input fields
pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1)
glucose = st.number_input("Glucose Level", min_value=0, max_value=300, value=120)
blood_pressure = st.number_input("Blood Pressure", min_value=0, max_value=200, value=80)
skin_thickness = st.number_input("Skin Thickness", min_value=0, max_value=100, value=20)
insulin = st.number_input("Insulin Level", min_value=0, max_value=1000, value=80)
bmi = st.number_input("BMI", min_value=0.0, max_value=50.0, value=25.0, step=0.1)
dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.5, step=0.01)
age = st.number_input("Age", min_value=0, max_value=120, value=30)

# Predict button
if st.button("Predict"):
    # Prepare input data
    input_data = {
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": blood_pressure,
        "SkinThickness": skin_thickness,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": dpf,
        "Age": age,
    }

    # Call Flask API
    try:
        response = requests.post(FLASK_API_URL, json=input_data)
        result = response.json()

        # Display the result
        if "error" in result:
            st.error(f"❌ Error: {result['error']}")
        else:
            prediction = result["prediction"]
            probability = result["probability"]

            if prediction == "Diabetes":
                st.error(f"🚨 High Risk: {prediction} (Confidence: {probability:.2f})")
            else:
                st.success(f"✅ Low Risk: {prediction} (Confidence: {probability:.2f})")

    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")