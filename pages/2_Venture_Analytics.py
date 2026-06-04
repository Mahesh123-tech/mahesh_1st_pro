import streamlit as st
import plotly.express as px
import pandas as pd
from utils.loader import load_data

st.set_page_config(page_title="Venture Analytics", layout="wide")
df = load_data()

st.title("💸 Capital Consumption & Investor Telemetry")
st.markdown("Assessing market sizes, capitalization matrices, and deployment efficiency pathways.")

st.markdown("### Burn Rate vs Topline Annual Revenue Generations")
st.caption("Scatter sample space restricted to 5,000 rows for high-fps UI interaction performance.")
fig_scatter = px.scatter(
    df.sample(5000, random_state=42),
    x="burn_rate_million",
    y="revenue_million",
    color="outcome",
    size="team_size",
    hover_data=["sector", "funding_rounds"],
    color_discrete_map={'Failure': '#EF4444', 'IPO': '#3B82F6', 'Acquisition': '#10B981'},
    labels={"burn_rate_million": "Burn Rate ($ Millions / Yr)", "revenue_million": "Annual Topline Revenue ($ Millions)"}
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.write("---")
c1, c2 = st.columns(2)

with c1:
    st.markdown("### Exit Allocation by Investor Segment")
    investor = pd.crosstab(df["investor_type"], df["outcome"])
    fig_bar = px.bar(investor, barmode="group", color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_bar, use_container_width=True)
    
    best_investor = df[df["outcome"] == "IPO"].groupby("investor_type").size().idxmax()
    st.success(f"🏆 **Dominant Vehicle Category:** Peak IPO generations cluster around **{best_investor}** institutions.")

with c2:
    st.markdown("### Operational Revenue Variance Analysis")
    fig_violin = px.violin(df, x="outcome", y="revenue_million", box=True, color="outcome")
    st.plotly_chart(fig_violin, use_container_width=True)
