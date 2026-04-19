# =====================================
# IMPORT LIBRARIES
# =====================================
import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Car Price Predictor",
    layout="centered",
    page_icon="🚗"
)

# =====================================
# LOAD MODEL
# =====================================
model = pickle.load(open('car_price_model.pkl', 'rb'))

# =====================================
# TITLE
# =====================================
st.markdown("<h1 style='text-align: center;'>🚗 Car Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Predict the resale value of your car using Machine Learning</p>", unsafe_allow_html=True)
st.markdown("---")

# =====================================
# INPUT SECTION
# =====================================
col1, col2 = st.columns(2)

with col1:
    present_price = st.number_input("💰 Present Price (Lakhs)", min_value=0.0, value=5.0)
    kms_driven = st.number_input("📍 KMs Driven", min_value=0, value=30000)
    owner = st.selectbox("👤 Previous Owners", [0, 1, 2, 3])

with col2:
    fuel = st.selectbox("⛽ Fuel Type", ["Petrol", "Diesel"])
    seller = st.selectbox("🏪 Seller Type", ["Dealer", "Individual"])
    transmission = st.selectbox("⚙️ Transmission", ["Manual", "Automatic"])
    year = st.number_input("📅 Year of Purchase", min_value=2000, max_value=2026, value=2018)

st.markdown("---")

# =====================================
# FEATURE ENGINEERING
# =====================================
no_year = 2026 - year

fuel_diesel = 1 if fuel == "Diesel" else 0
fuel_petrol = 1 if fuel == "Petrol" else 0
seller_individual = 1 if seller == "Individual" else 0
trans_manual = 1 if transmission == "Manual" else 0

# =====================================
# PREDICTION
# =====================================
if st.button("🔍 Predict Price"):

    data = pd.DataFrame(
        [[present_price, kms_driven, owner, no_year,
          fuel_diesel, fuel_petrol,
          seller_individual, trans_manual]],
        columns=[
            'Present_Price',
            'Kms_Driven',
            'Owner',
            'no_year',
            'Fuel_Type_Diesel',
            'Fuel_Type_Petrol',
            'Seller_Type_Individual',
            'Transmission_Manual'
        ]
    )

    prediction = model.predict(data)[0]

    # =====================================
    # OUTPUT
    # =====================================
    st.success(f"💸 Estimated Selling Price: ₹ {prediction:.2f} Lakhs")

    # =====================================
    # INSIGHTS
    # =====================================
    if prediction > present_price:
        st.warning("⚠️ Unusual: Predicted price is higher than showroom price.")
    elif prediction < present_price * 0.5:
        st.info("📉 High depreciation detected.")
    else:
        st.info("✅ Normal depreciation range.")

    # =====================================
    # CHART (Depreciation Trend)
    # =====================================
    st.markdown("### 📊 Price Depreciation Trend")

    years = list(range(1, int(no_year) + 1))
    prices = [present_price * (0.9 ** i) for i in years]

    fig, ax = plt.subplots()
    ax.plot(years, prices)
    ax.set_xlabel("Years")
    ax.set_ylabel("Estimated Price (Lakhs)")
    ax.set_title("Car Value Over Time")

    st.pyplot(fig)
