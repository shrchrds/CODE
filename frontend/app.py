import streamlit as st
import pandas as pd
import requests # We're adding this now!

# --- Page Configuration ---
st.set_page_config(
    page_title="Project C.O.D.E.",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Initialize Session State ---
# This is crucial! We'll store all our app's data here.
# It persists across reruns.
if 'comparison_results' not in st.session_state:
    st.session_state.comparison_results = None

# --- Header ---
st.title("🚀 Project C.O.D.E.")
st.subheader("Your AI-Powered Career Offer Decision Engine")
st.markdown("Enter the details for two offers below to see a detailed financial comparison and a personalized alignment score.")
st.markdown("---")


# --- Sidebar for User Preferences ---
with st.sidebar:
    st.header("Your Preferences")
    st.markdown("Rate how important each factor is to you (1=Not important, 10=Very important).")
    
    # We use keys to easily access these values later
    pref_cash = st.slider("Year 1 Cash", 1, 10, 8, key="pref_cash")
    pref_value = st.slider("4-Year Total Value", 1, 10, 9, key="pref_value")
    pref_wlb = st.slider("Work-Life Balance", 1, 10, 9, key="pref_wlb")
    pref_growth = st.slider("Career Growth / Learning", 1, 10, 8, key="pref_growth")


# --- Main Layout & Input Forms ---
# Using st.form prevents the app from rerunning on every widget interaction.
# Data is only sent when the 'st.form_submit_button' is clicked.
with st.form("comparison_form"):
    col1, col2 = st.columns(2)

    with col1:
        st.header("Offer 1")
        c1_name = st.text_input("Company Name", "Google", key="c1_name")
        c1_ticker = st.text_input("Stock Ticker", "GOOGL", key="c1_ticker")
        c1_base = st.number_input("Base Salary (INR)", min_value=0, value=4000000, step=100000, key="c1_base")
        c1_bonus = st.number_input("Target Bonus (%)", min_value=0, value=15, key="c1_bonus")
        c1_signon = st.number_input("Joining Bonus (INR)", min_value=0, value=500000, step=50000, key="c1_signon")
        c1_rsu = st.number_input("4-Year RSU Grant (USD)", min_value=0, value=80000, step=1000, key="c1_rsu")

    with col2:
        st.header("Offer 2")
        c2_name = st.text_input("Company Name", "Microsoft", key="c2_name")
        c2_ticker = st.text_input("Stock Ticker", "MSFT", key="c2_ticker")
        c2_base = st.number_input("Base Salary (INR)", min_value=0, value=3800000, step=100000, key="c2_base")
        c2_bonus = st.number_input("Target Bonus (%)", min_value=0, value=20, key="c2_bonus")
        c2_signon = st.number_input("Joining Bonus (INR)", min_value=0, value=800000, step=50000, key="c2_signon")
        c2_rsu = st.number_input("4-Year RSU Grant (USD)", min_value=0, value=100000, step=1000, key="c2_rsu")

    # The submit button for the form
    submitted = st.form_submit_button("✨ Compare Offers!", use_container_width=True)


# --- API Call and Data Processing ---
# This block of code only runs when the form's submit button is clicked.
if submitted:
    # 1. Structure the data into the format our API expects.
    api_payload = {
        "offers": [
            {
                "company_name": c1_name,
                "stock_ticker": c1_ticker,
                "base_salary": c1_base,
                "bonus_percent": c1_bonus,
                "joining_bonus": c1_signon,
                "rsu_grant_usd": c1_rsu
            },
            {
                "company_name": c2_name,
                "stock_ticker": c2_ticker,
                "base_salary": c2_base,
                "bonus_percent": c2_bonus,
                "joining_bonus": c2_signon,
                "rsu_grant_usd": c2_rsu
            }
        ],
        "preferences": {
            "year_1_cash": pref_cash,
            "four_year_value": pref_value,
            "work_life_balance": pref_wlb,
            "career_growth": pref_growth
        }
    }
    
    # 2. Show a spinner while we wait for the API response.
    with st.spinner('Analyzing offers...'):
        try:
            # IMPORTANT: Replace this with your actual Render URL
            api_url = "https://project-code-backend.onrender.com/api/v1/compare"
            
            response = requests.post(api_url, json=api_payload)
            response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)
            
            # 3. Store the successful response in session state.
            st.session_state.comparison_results = response.json()
            
        except requests.exceptions.RequestException as e:
            st.error(f"Error calling API: {e}")
            st.session_state.comparison_results = None # Clear old results on error


# --- Display Results ---
# This block runs every time, but only shows content if results are available.
if st.session_state.comparison_results:
    st.markdown("---")
    st.header("Comparison Results")
    
    results_data = st.session_state.comparison_results.get('results', [])
    
    if results_data:
        # For now, let's just display the raw JSON to confirm we received it.
        st.success("Analysis complete! Here are the results:")
        st.json(st.session_state.comparison_results)
    else:
        st.warning("The API returned no results to display.")
