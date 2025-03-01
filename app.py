import streamlit as st
import datetime
import requests
import json
import pandas as pd
from menu import create_menu
import matplotlib.pyplot as plt
import time
from graphs.plots import create_category_sales_chart, moth_category_name



st.set_page_config(layout="wide")

# Create the custom navbar
create_menu()

st.title("Table for predictions")

endpoint_get = 'http://127.0.0.1:8000/predict'


if st.button('Fetch Data'):
    try:
        response = requests.get(endpoint_get)
        response.raise_for_status()  # Raise an exception for bad status codes
        req_prediction = response.json()
        data = json.loads(req_prediction)
        df = pd.DataFrame(data)
        
        print(df)
        st.success('Data fetched successfully!')
        fig, grouped_data = create_category_sales_chart(df)

        # Display the chart in Streamlit
        st.pyplot(fig)

        # Display the grouped data
        st.write("Grouped Data:")
        st.dataframe(grouped_data)
        

        # st.table(df)
        # st.json(data)
    except requests.RequestException as e:
        st.error(f'Error fetching data: {str(e)}')
        
        
# while True:
#     # Your app code here
#     st.write("This will update every 5 seconds")
    
#     # Wait for 5 seconds
#     time.sleep(5)
    
#     # Rerun the app
#     st.experimental_rerun()

