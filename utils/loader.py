import streamlit as st
import pandas as pd
import os

def process_dataframe(df):
    # Standardize revenue formatting if raw data is absolute dollars instead of millions
    if 'revenue_million' in df.columns and df['revenue_million'].max() > 100000:
        df['revenue_million'] = df['revenue_million'] / 1_000_000
    return df

def load_data():
    # Share dataset across all sub-pages once loaded into session state
    if "cached_df" in st.session_state:
        return st.session_state["cached_df"]
        
    file_path = "data/startup_success_dataset.csv"
    
    # Attempt to read from the GitHub repository folder
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            df = pd.read_csv(file_path)
            df = process_dataframe(df)
            st.session_state["cached_df"] = df
            return df
        except Exception:
            pass # Fall through to uploader if parsing fails
            
    # Fail-safe Interactive Interface if the GitHub file is empty or missing
    st.warning("⚠️ **Data Stream Interrupted:** The repository file `data/startup_success_dataset.csv` is currently empty (0 bytes) or missing on GitHub.")
    st.markdown("### 📥 Temporary Application Activation Panel")
    st.markdown("To interact with your application immediately, drag and drop your local copy of **`startup_success_dataset (1).csv`** below. It will temporarily activate the multi-page engine while you fix the repository.")
    
    uploaded_file = st.file_uploader("Upload your startup dataset CSV", type=["csv"], key="repo_fallback_uploader")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            df = process_dataframe(df)
            st.session_state["cached_df"] = df
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error parsing uploaded file: {e}")
            st.stop()
    else:
        st.stop() # Stops execution gracefully until the file is provided
