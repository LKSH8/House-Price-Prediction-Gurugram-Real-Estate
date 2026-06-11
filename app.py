import streamlit as st
import pickle
import pandas as pd
import streamlit.components.v1 as components

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid username or password")

if not st.session_state.logged_in:
    login()
    st.stop()

st.set_page_config(
    page_title="Gurgaon Flat Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# Load model
with open("house_price_model.pkl", "rb") as file:
    model = pickle.load(file)

# Load column order
with open("columns.pkl", "rb") as file:
    columns = pickle.load(file)

# Load dataset
df = pd.read_csv("FLAT_GGN_FINAL_FIXED_MEDIAN.csv")

st.title("Gurgaon Flat Price Predictor")
st.write("Enter flat details and predict the estimated price in Gurgaon.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏡 Property Details")

    area = st.number_input("Area in sqft", min_value=100, value=1500)
    bedRoom = st.number_input("Bedrooms", min_value=1, value=3)
    bathroom = st.number_input("Bathrooms", min_value=1, value=3)
    balcony = st.number_input("Balconies", min_value=0, value=2)
    floorNum = st.number_input("Floor Number", min_value=0, value=5)
    agePossession = st.number_input("Age of Property", min_value=0, value=5)

with col2:
    st.subheader("✨ Extra Features")

    study_room = st.selectbox("Study Room", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    servant_room = st.selectbox("Servant Room", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    store_room = st.selectbox("Store Room", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    pooja_room = st.selectbox("Pooja Room", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    others = st.selectbox("Other Room", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

    furnishing_type = st.selectbox(
        "Furnishing Type",
        [0, 1, 2],
        format_func=lambda x: {
            0: "Unfurnished",
            1: "Semi-Furnished",
            2: "Furnished"
        }[x]
    )

st.divider()

st.subheader("📍 Sector Details")

sector_input = st.number_input("Enter Gurgaon Sector Number", min_value=1, value=56)

sector_median_price = df[df["sector_number"] == sector_input]["sector_median_price"].max()

if pd.isna(sector_median_price):
    st.error("Sector not found in dataset.")
    st.stop()

st.info(f"Sector {sector_input} Median Price: ₹{sector_median_price} crore")

st.divider()

if st.button("🔮 Predict Price", use_container_width=True):
    input_data = pd.DataFrame(
        [[
            area,
            bedRoom,
            bathroom,
            balcony,
            floorNum,
            agePossession,
            study_room,
            servant_room,
            store_room,
            pooja_room,
            others,
            furnishing_type,
            sector_median_price
        ]],
        columns=columns
    )

    prediction = model.predict(input_data)[0]

    st.success(f"Estimated Flat Price: ₹{prediction:.2f} crore")

st.divider()

st.subheader("🗺️ Sector Location on Map")

components.iframe(
    f"https://maps.google.com/maps?q=Sector%20{sector_input}%20Gurgaon&z=13&output=embed",
    height=450,
    width=1000
)