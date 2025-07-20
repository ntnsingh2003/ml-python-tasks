import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Set custom page config
st.set_page_config(
    page_title="Placement Package Predictor",
    layout="wide",
)

# Add background with CSS
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(to right top, #1e3c72, #2a5298);
    background-size: cover;
    color: white;
}
[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
}
div.stButton > button {
    color: white;
    background-color: #2a5298;
    border-radius: 8px;
    padding: 0.5em 1em;
}
.stSlider > div {
    color: white;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; color: white;'>📊 Placement Package Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Enter your skills and academics to estimate your expected placement package (LPA).</p>", unsafe_allow_html=True)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("pkg.csv")

data = load_data()

# Feature setup
features = [
    "Technical Skills",
    "DSA",
    "CS Core Subjects",
    "Projects & Internships",
    "CGPA",
    "Communication & Soft Skills",
    "College Tier"
]
target = "Package in LPA"

# Train Linear Regression model
X = data[features]
y = data[target]

model = LinearRegression()
model.fit(X, y)
r2 = r2_score(y, model.predict(X))

# Input form
st.markdown("---")
st.subheader("🎯 Input Your Ratings (0-10 Scale)")

col1, col2, col3 = st.columns(3)
with col1:
    tech = st.slider("Technical Skills", 0.0, 10.0, 7.0)
    dsa = st.slider("DSA", 0.0, 10.0, 7.0)
    core = st.slider("CS Core Subjects", 0.0, 10.0, 7.0)
with col2:
    proj = st.slider("Projects & Internships", 0.0, 10.0, 7.0)
    cgpa = st.slider("CGPA", 0.0, 10.0, 7.5)
    comm = st.slider("Communication & Soft Skills", 0.0, 10.0, 7.0)
with col3:
    tier = st.selectbox("College Tier (1 = Top Tier, 3 = Lower Tier)", [1, 2, 3])
    submit = st.button("🔍 Predict Package")

# Predict
if submit:
    user_input = pd.DataFrame([[tech, dsa, core, proj, cgpa, comm, tier]], columns=features)
    prediction = model.predict(user_input)[0]
    st.markdown("---")
    st.success(f"💼 **Estimated Package:** ₹{prediction:.2f} LPA")
    st.caption(f"📈 Model Accuracy (R² Score): `{r2:.2f}`")

# Optional: Show data preview
with st.expander("📂 Show Training Data"):
    st.dataframe(data.head(20))
