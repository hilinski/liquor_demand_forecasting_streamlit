import streamlit as st
import requests


'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

date = st.date_input('Date input')
time = st.time_input('Time entry')
p_lon = st.number_input('Pickup Longitude')
p_lat = st.number_input('Pickup Latitude')
d_lon = st.number_input('Dropoff Longitude')
d_lat = st.number_input('Dropoff Latitude')
pax = st.selectbox('Pax', [i for i in range(1,11)])


'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''

mydict = {'pickup_datetime': f"{date} {time}",
          'pickup_longitude': p_lon,
          'pickup_latitude': p_lat,
          'dropoff_longitude': d_lon,
          'dropoff_latitude': d_lat,
          'passenger_count': pax
          }

mydict


if st.button('Estimar Precio',icon="😃", ):
    data = requests.get(url,params=mydict).json()
    st.write(f"EL precio estimado es: {data['fare']}")
