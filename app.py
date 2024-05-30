from datetime import datetime

import requests
import streamlit as st


@st.cache_data
def get_photo_url():
    pexels_api_url = st.secrets.get('pexels_api_url')
    pexels_api_key=st.secrets.get('pexels_api_key')
    pexels_photo_id=st.secrets.get('pexels_photo_id')
    
    response = requests.get(f"{pexels_api_url}/{pexels_photo_id}", headers={"Authorization":pexels_api_key}).json()
    return response['src']['original']

background_image = get_photo_url()

CSS = f'''
h1 {{
    color: yellow;
    margin-bottom: 2rem;
}}
.stApp {{
    background-image: linear-gradient(to right bottom, rgba(0, 0, 0, .75), rgba(141, 150, 54, .65)), url({background_image});
    background-size: cover;
}}
'''

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

'''
# 🚕 New York Taxifare prediction

'''

col5, col6, col7 = st.columns(3)
with col5:
    pickup_date = st.date_input('pickup date')

with col6:
    pickup_time = st.time_input("pickup time")

with col7:
    passenger_count = st.number_input('passenger count', step=0, min_value=1)


col1, col2 = st.columns(2)
with col1:
    pickup_longitude = st.number_input('pickup longitude')

with col2:
    pickup_latitude = st.number_input('pickup latitude')

col3, col4 = st.columns(2)
with col3:
    dropoff_longitude = st.number_input('dropoff longitude')

with col4:
    dropoff_latitude = st.number_input('dropoff latitude')



pickup_datetime = datetime.strptime(f"{pickup_date} {pickup_time}", "%Y-%m-%d %H:%M:%S")

data = dict(
    pickup_datetime=pickup_datetime,
    dropoff_longitude=dropoff_longitude,
    dropoff_latitude=dropoff_latitude,
    pickup_longitude=pickup_longitude,
    pickup_latitude=pickup_latitude,
    passenger_count=passenger_count,
)

with st.echo():
    st.write(data)

is_predict_disabled: bool = bool(pickup_date and pickup_time and pickup_longitude and passenger_count and dropoff_latitude and dropoff_longitude)

if st.button('predict', disabled=not is_predict_disabled, type="secondary"):
    url = st.secrets.get('api_url')
    response = requests.get(url, params=data)
    result = response.json()
    st.write(result)

