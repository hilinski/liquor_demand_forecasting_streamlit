import streamlit as st
import datetime
import requests
import json
import pandas as pd
from menu import create_menu
import matplotlib.pyplot as plt
import time
from graphs.plots import create_weekly_sales_chart, multiple_categories_chat


st.set_page_config(layout="wide")

# Create the custom navbar
create_menu()

st.title("Table for predictions")


selected_year = st.selectbox('Select a year:', ['2022', '2023', '2024'])

if st.button('Fetch Data'):
    try:
        endpoint_get = f'http://127.0.0.1:8000/pred-year?year_pred={selected_year}'
        categories = ['RUM', 'VODKA', 'WHISKY', 'TEQUILA_MEZCAL', 'LIQUEURS', 'OTROS', 'GIN']
        year_conversor = int(selected_year) - 3; 
        response = requests.get(endpoint_get)
         # Raise an exception for bad status codes
        response.raise_for_status() 
        
        req_prediction = response.json()
        data = json.loads(req_prediction[0])
        data_mae = json.loads(req_prediction[1])
        df = pd.DataFrame(data)
        
        df_mae = pd.DataFrame(data_mae) 
        
        st.success('Data fetched successfully!')

        fig, grouped_data = create_weekly_sales_chart(df, start_year=year_conversor)
        fig2, grouped_data2 = multiple_categories_chat(df, categories)

        st.pyplot(fig, clear_figure=True)
        
        st.title("Prediction per Categorie")
        st.pyplot(fig2, clear_figure=True)
        
        
        st.title("Model Error Validation")
        st.dataframe(df_mae)
        
        # st.table(df)
        # st.json(data)
    except requests.RequestException as e:
        st.error(f'Error fetching data: {str(e)}')
        