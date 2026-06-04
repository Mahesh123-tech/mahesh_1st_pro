import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from utils.loader import load_data

st.set_page_config(page_title="Success Predictor", layout="wide")
df = load_data()

st.title("🤖 Predict Predictive Risk & Success Factors")
st.markdown("Training a downstream Ensemble Forest classifier over global records to evaluate predictive weight vector metrics.")

# 1. Pipeline Processing Initialization
@st.cache_resource
def train_pipeline_model():
    data = df.copy()
    cat_cols = ["sector", "investor_type", "founder_background"]
    
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        encoders[col] = le
        
    X = data.drop(["outcome"], axis=1)
    y = data["outcome"]
    
    rf = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
    rf.fit(X, y)
    
    return rf, X.columns

model, feature_names = train_pipeline_model()

# 2. Dynamic Feature Importance Layout Plot
st.markdown("### Feature Importance Matrix (Success Drivers)")
importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Calculated Vector Importance": model.feature_importances_
}).sort_values("Calculated Vector Importance", ascending=True)

fig = px.bar(
    importance_df, 
    x="Calculated Vector Importance", 
    y="Feature", 
    orientation="h",
    color="Calculated Vector Importance",
    color_continuous_scale="Purples"
)
st.plotly_chart(fig, use_container_width=True)

# 3. Execution Simulation Interface
st.write("---")
st.markdown("### Operational Risk Simulation Matrix")
st.caption("Input structural parameters manually below to inspect predictive tracking classifications.")

sc1, sc2, sc3 = st.columns(3)
with sc1:
    in_rounds = st.number_input("Funding Rounds Completed", min_value=1, max_value=10, value=2)
    in_exp = st.slider("Founder Domain Longevity (Years)", 0, 30, 10)
with sc2:
    in_team = st.number_input("Total Corporate Team Size", min_value=1, max_value=2000, value=50)
    in_tam = st.number_input("Total Addressable Market ($ Billions)", min_value=0.1, max_value=500.0, value=15.0)
with sc3:
    in_burn = st.number_input("Current Annual Burn Rate ($ Millions)", min_value=0.0, max_value=100.0, value=5.0)
    in_rev = st.number_input("Current Topline Annual Revenue ($ Millions)", min_value=0.0, max_value=1000.0, value=2.5)

# Setup simulated user inference row matching encoding formats
sim_row = pd.DataFrame([{
    "funding_rounds": in_rounds,
    "founder_experience_years": in_exp,
    "team_size": in_team,
    "market_size_billion": in_tam,
    "product_traction_users": 150000, # control static median proxy
    "burn_rate_million": in_burn,
    "revenue_million": in_rev,
    "investor_type": 0,       # static baseline proxy indices
    "sector": 0,
    "founder_background": 0
}])

# Output Simulated Probabilities
probs = model.predict_proba(sim_row)[0]
classes = model.classes_

st.markdown("#### Simulated Real-time Diagnostic Matrix Outcomes")
res_cols = st.columns(len(classes))
for idx, cls in enumerate(classes):
    res_cols[idx].metric(label=f"Probability Profile: {cls}", value=f"{probs[idx]*100:.1f}%")
