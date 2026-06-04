import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    try:
        # Load the user's uploaded dataset
        df = pd.read_csv("data/startup_success_dataset (1).csv")
        
        # Standardize revenue display formats: convert to millions if row strings are unscaled
        if df['revenue_million'].max() > 100000:
            df['revenue_million'] = df['revenue_million'] / 1_000_000
            
        return df
    except FileNotFoundError:
        st.error("❌ Critical Asset Failure: 'data/startup_success_dataset (1).csv' not located.")
        st.stop()
