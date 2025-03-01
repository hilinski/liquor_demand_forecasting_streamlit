import streamlit as st
import datetime
import requests
import json
import pandas as pd
from menu import create_menu
import matplotlib.pyplot as plt
import time
from graphs.plots import create_weekly_sales_chart



st.set_page_config(layout="wide")

# Create the custom navbar
create_menu()

st.title("Table for line predictions")

endpoint_get = 'http://127.0.0.1:8000/predict'




if st.button('Fetch Data'):
    try:
        response = requests.get(endpoint_get)
        response.raise_for_status()  # Raise an exception for bad status codes
        req_prediction = response.json()
        data = json.loads(req_prediction)
        df = pd.DataFrame(data)
        
        
        fig, weekly_sales = create_weekly_sales_chart(df)
        
        st.success('Data fetched successfully!')
        st.pyplot(fig)
        st.write("Weekly Sales Data:")
        st.dataframe(weekly_sales)
        # print(df)

       
        # st.table(df)
        # st.json(data)
    except requests.RequestException as e:
        st.error(f'Error fetching data: {str(e)}')
        
