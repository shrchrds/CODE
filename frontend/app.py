# frontend/app.py
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Project C.O.D.E. - MVP",
    layout="wide"
)

st.title("🚀 Welcome to Project C.O.D.E!")
st.header("Your Career Offer Decision Engine")

st.markdown("""
    This is the future home of your intelligent career co-pilot.
    Right now, it's just a simple 'Hello World' to make sure everything is deployed correctly.
""")

# Let's add a little interactive element to prove it's a real Streamlit app
st.subheader("Check Is app Ready?")

df = pd.DataFrame(
   np.random.randn(10, 2),
   columns=['Col A', 'Col B'])
   
st.line_chart(df)

st.success("Hare Krishna!")