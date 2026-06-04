import streamlit as st
from utils.loader import load_data

st.set_page_config(
    page_title="Startup Success Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional UI Theme Injection
st.markdown("""
<style>
    .main { background: #F8FAFC; }
    div[data-testid="metric-container"] {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
    }
    .block-container { padding-top: 2rem; }
    h1, h2, h3 { color: #1E293B; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Startup Success Intelligence Platform")
st.markdown("""
Welcome to the enterprise execution control panel. This system utilizes advanced data infrastructure, 
unsupervised clustering, and predictive random forest estimators to systematically analyze 100,000 global venture profiles.
""")
st.write("---")

# Preload data cache to globally assert health metrics
df = load_data()

# Global KPI calculations
c1, c2, c3, c4 = st.columns(4)
c1.metric("Global Cohort Size", f"{len(df):,}")
c2.metric("IPO Success Rate", f"{(df['outcome'].eq('IPO').mean()*100):.2f}%")
c3.metric("M&A Acquisition Rate", f"{(df['outcome'].eq('Acquisition').mean()*100):.2f}%")
c4.metric("Failure Capital Deficit", f"{(df['outcome'].eq('Failure').mean()*100):.2f}%")

st.info("👈 Select an analytical matrix module from the sidebar interface to begin deep evaluation.")
