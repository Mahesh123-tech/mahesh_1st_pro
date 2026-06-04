import streamlit as st
import plotly.express as px
import pandas as pd
from utils.loader import load_data

st.set_page_config(page_title="Executive Dashboard", layout="wide")
df = load_data()

st.title("📊 Executive Strategic Overview")
st.markdown("Macro sector performance indicators, distributions, and correlation frameworks.")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### Global Outcome Trajectories")
    fig1 = px.pie(df, names="outcome", hole=0.5, color_discrete_sequence=px.colors.qualitative.Safe)
    fig1.update_layout(margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.markdown("### Cross-Industry Success Distribution")
    heat = pd.crosstab(df["sector"], df["outcome"])
    fig2 = px.imshow(heat, text_auto=True, color_continuous_scale="Viridis")
    st.plotly_chart(fig2, use_container_width=True)

st.write("---")
st.markdown("### Feature Interactions Profile")
num_cols = df.select_dtypes(include=["int64", "float64"]).columns
corr = df[num_cols].corr()
fig3 = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r")
st.plotly_chart(fig3, use_container_width=True)
