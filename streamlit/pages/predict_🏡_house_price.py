import streamlit as st
import requests
import pandas as pd
import os

# Configure the page
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏡",
)

#####Sidebar Start#####

# Add a sidebar
st.sidebar.markdown("### **Fill in property details and predict the house price**")
st.sidebar.image(os.path.join('pages', 'house.jpg'), use_column_width=True)

# Define the possible values for each column
property_subtypes_house = [
    "HOUSE", "MIXED_USE_BUILDING", "APARTMENT_BLOCK", "BUNGALOW", "VILLA", "EXCEPTIONAL_PROPERTY",
    "COUNTRY_COTTAGE", "MANSION", "FARMHOUSE", "TOWN_HOUSE", "MANOR_HOUSE", "CHALET", "OTHER_PROPERTY"
]

kitchen_types_house = [
    "INSTALLED", "USA_HYPER_EQUIPPED", "NOT_INSTALLED", "HYPER_EQUIPPED", "SEMI_EQUIPPED",
    "USA_SEMI_EQUIPPED", "USA_INSTALLED", "USA_UNINSTALLED"
]

state_of_buildings = [
    "GOOD", "AS_NEW", "TO_BE_DONE_UP", "TO_RENOVATE", "JUST_RENOVATED", "TO_RESTORE", "nan"
]

provinces = [
    "oost-vlaanderen", "luik", "waals-brabant", "antwerpen", "brussel", "vlaams-brabant", "henegouwen",
    "west-vlaanderen", "limburg", "luxemburg", "namen"
]


#_____postal codes preparation_______
# Load the data from the CSV file
pc = pd.read_csv(os.path.join('pages','house_pc_city.csv'))

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
data['property_subtype'] = st.selectbox("Property Subtype", property_subtypes_house)
data['number_of_rooms'] = st.slider("Number of Rooms", min_value=0, max_value=32, step=1)
data['living_area'] = st.slider("Living Area", min_value=14, max_value=395, step=1)
data['kitchen_type'] = st.selectbox("Kitchen Type", kitchen_types_house)
data['furnished'] = st.toggle('Furnished')
data['open_fire'] = st.toggle('Open Fire')
data['terrace'] = st.toggle('Terrace')
data['terrace_area'] = st.slider("Terrace Area", min_value=0, max_value=2771, step=1)
data['garden'] = st.toggle('Garden')
data['garden_area'] = st.slider("Garden Area", min_value=0, max_value=23051, step=1)
data['surface_of_good'] = st.slider("Surface of Good", min_value=0, max_value=999999, step=1)
data['number_of_facades'] = st.slider("Number of Facades", min_value=0, max_value=8, step=1)
data['swimming_pool'] = st.toggle('Swimming Pool')
data['state_of_building'] = st.selectbox("State of Building", state_of_buildings)
data['province'] = st.selectbox("Province", provinces)

# make a button to predict
if st.button('Predict'):
    st.subheader("House price prediction")
    res = requests.post(url = "https://immo-eliza-deployment-yr5r.onrender.com/predict/house", json=data)
    cleaned_prediction = float(res.text.strip("[]"))
    if res.status_code == 200:
        st.write(f"€{round(cleaned_prediction,2)}")
    else:
        st.write("Prediction failed. Please check your input and try again.")