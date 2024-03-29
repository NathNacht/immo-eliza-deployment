import streamlit as st
import requests
import pandas as pd
import os

# Configure the page
st.set_page_config(
    page_title="Apartment Price Prediction",
    page_icon="🏬",
)

#####Sidebar Start#####

# Add a sidebar
st.sidebar.markdown("### **Fill in property details and predict the apartment price**")
st.sidebar.image(os.path.join('pages', 'apartment.jpg'), use_column_width=True)

# Define the possible values for each column
property_subtypes_apartment = [
    "FLAT_STUDIO", "APARTMENT", "DUPLEX", "GROUND_FLOOR", "PENTHOUSE", "SERVICE_FLAT", "LOFT", "TRIPLEX", "KOT"
]

kitchen_types_apartment = [
    "NOT_INSTALLED", "USA_SEMI_EQUIPPED", "INSTALLED", "SEMI_EQUIPPED", "HYPER_EQUIPPED", "USA_INSTALLED",
    "USA_HYPER_EQUIPPED", "USA_UNINSTALLED"
]

state_of_buildings = [
    "GOOD", "AS_NEW", "TO_BE_DONE_UP", "TO_RENOVATE", "JUST_RENOVATED", "TO_RESTORE"
]

provinces = [
    "oost-vlaanderen", "luik", "waals-brabant", "antwerpen", "brussel", "vlaams-brabant", "henegouwen",
    "west-vlaanderen", "limburg", "luxemburg", "namen"
]


#_____postal codes preparation_______
# Load the data from the CSV file
pc = pd.read_csv(os.path.join('pages','app_pc_city.csv'))


# Get the unique postal codes
unique_postal_codes = pc['postal_code'].unique()

# Create a dictionary mapping postal codes to main cities
postal_code_map = pc.set_index('postal_code')['main_city'].to_dict()


# Define the layout in two columns
# left_column, right_column = st.columns([1, 1])

# with left_column:

data = {}

selected_postal_code = st.selectbox('Select a postal code', unique_postal_codes)
data['postal_code'] = str(selected_postal_code)        
selected_main_city = postal_code_map.get(selected_postal_code)
st.sidebar.write(f"Selected postal code: {selected_postal_code}")
st.sidebar.write(f"Main city: {selected_main_city}")    

data['property_subtype'] = st.selectbox("Property Subtype", property_subtypes_apartment)
data['number_of_rooms'] = st.slider("Number of Rooms", min_value=0, max_value=22, step=1)
data['living_area'] = st.slider("Living Area", min_value=0, max_value=286, step=1)
data['kitchen_type'] = st.selectbox("Kitchen Type", kitchen_types_apartment)
data['furnished'] = st.toggle('Furnished')
data['open_fire'] = st.toggle('Open Fire')
data['terrace'] = st.toggle('Terrace')
data['terrace_area'] = st.slider("Terrace Area", min_value=0, max_value=814, step=1)
data['garden'] = st.toggle('Garden')
data['garden_area'] = st.slider("Garden Area", min_value=0, max_value=60000, step=1)
data['number_of_facades'] = st.slider("Number of Facades", min_value=0, max_value=5, step=1)
data['swimming_pool'] = st.toggle('Swimming Pool')
data['state_of_building'] = st.selectbox("State of Building", state_of_buildings)
data['province'] = st.selectbox("Province", provinces)

# make a button to predict
if st.button('Predict'):
    st.subheader("Apartment price prediction")
    res = requests.post(url = "https://immo-eliza-deployment-yr5r.onrender.com/predict/apartment", json=data)
    cleaned_prediction = float(res.text.strip("[]"))
    if res.status_code == 200:
        st.write(f"€{round(cleaned_prediction,2)}")
    else:
        st.write("Prediction failed. Please check your input and try again.")