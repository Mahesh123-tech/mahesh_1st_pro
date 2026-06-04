import streamlit as st
import plotly.express as px
from utils.loader import load_data

st.set_page_config(page_title="Founder Analytics", layout="wide")
df = load_data()

st.title("🧠 Human Capital Index & Market Funnels")
st.markdown("Correlating leadership longevity profiles against exit conversions.")

col_l, col_r = st.columns(2)

with col_l:
    st.markdown("### Industry Domain Longevity vs Outcome")
    fig_box = px.box(df, x="outcome", y="founder_experience_years", color="outcome")
    st.plotly_chart(fig_box, use_container_width=True)
    
    avg_exp = df.groupby("outcome")["founder_experience_years"].mean()
    st.info(f"""
    💡 **Mean Executive Domain Experience:**
    - **IPO Founders:** Average {avg_exp['IPO']:.1f} years experience
    - **Failure Subsets:** Average {avg_exp['Failure']:.1f} years experience
    """)

with col_r:
    st.markdown("### Ecosystem Exit Conversion Funnel")
    funnel_data = dict(
        stage=["Ecosystem Base", "Acquired", "IPO Target"],
        count=[len(df), (df["outcome"] == "Acquisition").sum(), (df["outcome"] == "IPO").sum()]
    )
    fig_funnel = px.funnel(funnel_data, x="count", y="stage", color_discrete_sequence=["#636EFA"])
    st.plotly_chart(fig_funnel, use_container_width=True)

st.write("---")
st.markdown("### Topline Revenue Generation Profiles")
top_sector = df.groupby("sector")["revenue_million"].mean().idxmax()
top_founder = df.groupby("founder_background")["revenue_million"].mean().idxmax()

s1, s2 = st.columns(2)
s1.success(f"🏢 **Top Yield Vertical (Mean Revenue):** {top_sector}")
s2.info(f"🧬 **Top Yield Archetype (Mean Revenue):** {top_founder}")
