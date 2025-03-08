import streamlit as st

def create_menu():
    # Custom CSS for horizontal navbar
    st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
    }
    .stButton {
        display: inline-block;
        width: 33.33%;
        padding: 0 5px;
        box-sizing: border-box;
    }
    div.row-widget.stHorizontal {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
    }
    [data-testid="stSidebar"][aria-expanded="true"] {display: none;}
    [data-testid="stSidebar"][aria-expanded="false"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

    # Create horizontal layout
    col1, col2, col3 = st.columns(3)

    # Add page links to each column
    with col1:
        st.page_link("pages/filter.py", label="Predicción", icon="🥃")
    with col2:
        st.page_link("pages/features.py", label="Predicción Por Año", icon="🚀")
    # with col3:

        
        
# # Use the create_menu function in your main app
# if __name__ == "__main__":
#     st.set_page_config(layout="wide")
#     create_menu()
#     st.title("Welcome to the Main Page")