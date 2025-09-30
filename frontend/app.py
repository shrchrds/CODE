import streamlit as st
import pandas as pd
# We will need 'requests' soon to call our API
# import requests 

# --- Page Configuration ---
st.set_page_config(
    page_title="Project C.O.D.E.",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Header ---
st.title("🚀 Project C.O.D.E.")
st.subheader("Your AI-Powered Career Offer Decision Engine")
st.markdown("---")

# --- Main Layout ---
# We'll use two columns for side-by-side offer comparison
col1, col2 = st.columns(2)

with col1:
    st.header("Offer 1")
    st.text_input("Company Name", key="company_1")
    st.number_input("Base Salary (INR)", min_value=0, key="base_1")
    # ... we will add more fields here ...

with col2:
    st.header("Offer 2")
    st.text_input("Company Name", key="company_2")
    st.number_input("Base Salary (INR)", min_value=0, key="base_2")
    # ... we will add more fields here ...


# --- Sidebar for User Preferences ---
with st.sidebar:
    st.header("Your Preferences")
    st.markdown("Rate how important each factor is to you (1=Not important, 10=Very important).")
    
    st.slider("Year 1 Cash", 1, 10, 8, key="pref_cash")
    st.slider("4-Year Total Value", 1, 10, 9, key="pref_value")
    st.slider("Work-Life Balance", 1, 10, 9, key="pref_wlb")
    st.slider("Career Growth / Learning", 1, 10, 8, key="pref_growth")

# --- Action Button ---
st.markdown("---")
if st.button("✨ Compare Offers!", use_container_width=True):
    st.success("Button clicked! Now we need to collect the data and call the API.")
    # We will add the logic to call the backend here