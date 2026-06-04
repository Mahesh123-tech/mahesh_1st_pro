import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
from utils.loader import load_data

st.set_page_config(page_title="Cohort Segmentation", layout="wide")
df = load_data()

st.title("🎯 Unsupervised Cohort Segmentation")
st.markdown("Utilizing KMeans algorithms to dynamically segment market actors by execution structures.")

# Isolate feature tracking dimensional arrays
cluster_features = ["funding_rounds", "team_size", "market_size_billion", "revenue_million"]
X = df[cluster_features]

# Execute clustering operation
kmeans = KMeans(n_clusters=4, random_state=42, n_init='auto')
df["cluster"] = kmeans.fit_predict(X)
df["cluster"] = df["cluster"].astype(str)

st.markdown("### Spatial Allocation Mapping (Cluster Spaces)")
fig = px.scatter(
    df.sample(5000, random_state=42),
    x="market_size_billion",
    y="revenue_million",
    color="cluster",
    hover_data=cluster_features,
    title="Structural Clusters mapped via Addressable Market vs Revenue Generations",
    color_discrete_sequence=px.colors.qualitative.D3
)
st.plotly_chart(fig, use_container_width=True)

# Generate algorithmic profile cards
st.markdown("### Cluster Characteristics Profile Matrix")
metrics_df = df.groupby("cluster")[cluster_features].mean()
st.dataframe(metrics_df, use_container_width=True)
