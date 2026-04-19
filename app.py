import streamlit as st
import pickle
import pandas as pd

# Load model
model = pickle.load(open('car_price_model.pkl', 'rb'))

st.title("🚗 Car Price Predictor")

# Inputs
present_price = st.number_input("Present Price (in Lakhs)")
kms_driven = st.number_input("KMs Driven")
owner = st.selectbox("Number of Previous Owners", [0,1,2,3])

fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel"])
seller = st.selectbox("Seller Type", ["Dealer", "Individual"])
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
year = st.number_input("Year of Purchase", min_value=2000, max_value=2026)

# Feature Engineering
no_year = 2026 - year

# Encoding
fuel_diesel = 1 if fuel == "Diesel" else 0
fuel_petrol = 1 if fuel == "Petrol" else 0
seller_individual = 1 if seller == "Individual" else 0
trans_manual = 1 if transmission == "Manual" else 0

# Prediction
if st.button("Predict Price"):
    data = pd.DataFrame([[present_price, kms_driven, owner, no_year,
                          fuel_diesel, fuel_petrol,
                          seller_individual, trans_manual]],
                        columns=['Present_Price','Kms_Driven','Owner','no_year',
                                 'Fuel_Type_Diesel','Fuel_Type_Petrol',
                                 'Seller_Type_Individual','Transmission_Manual'])

    prediction = model.predict(data)

    st.success(f"Estimated Selling Price: ₹ {prediction[0]:.2f} Lakhs")
