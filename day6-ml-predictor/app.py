import streamlit as st
import numpy as np
import pickle
import os

# -------------------------
# LOAD MODEL
# -------------------------
MODEL_FILE = os.path.join(os.path.dirname(__file__), "model.pkl")

with open(MODEL_FILE, "rb") as f:
    model = pickle.load(f)

# -------------------------
# PAGE CONFIG + HEADER UI
# -------------------------
st.set_page_config(
    page_title="CinePredict AI",
    page_icon="🎬",
    layout="centered"
)

st.markdown("""
<div style="
background: linear-gradient(90deg, #141414, #2b2b2b);
padding: 22px;
border-radius: 15px;
text-align: center;
color: white;
margin-bottom: 20px;
">
<h1>🎬 CinePredict AI</h1>
<p style="color: #bbbbbb;">Studio Intelligence Prediction System</p>
</div>
""", unsafe_allow_html=True)

# -------------------------
# INPUTS
# -------------------------
name = st.text_input("Enter your name")

if name:
    st.success(f"👋 Welcome, {name}")

industry = st.selectbox("Industry", ["Bollywood", "Hollywood"])

genre = st.selectbox(
    "Genre",
    ["Action", "Adventure", "Animation", "Drama", "Horror", "Romance", "Thriller"]
)

gross = st.number_input("Box office gross (crore INR)", value=500.0)
budget = st.number_input("Budget (USD)", value=20000000.0)

runtime = st.slider("Runtime (minutes)", 60, 240, 120)
popularity = st.slider("Popularity score (0-100)", 0, 100, 50)
month = st.selectbox("Release month", list(range(1, 13)))

# -------------------------
# ENCODING
# -------------------------
ind_map = {"Bollywood": 0, "Hollywood": 1}

genre_map = {
    "Action": 0,
    "Adventure": 1,
    "Animation": 2,
    "Drama": 3,
    "Horror": 4,
    "Romance": 5,
    "Thriller": 6
}

ind_enc = ind_map[industry]
genre_enc = genre_map[genre]

# -------------------------
# MODEL INPUT
# -------------------------
X = np.array([[
    ind_enc,
    gross,
    genre_enc,
    budget,
    runtime,
    popularity,
    month
]])

# -------------------------
# PREDICTION
# -------------------------
if st.button("🎬 Predict Outcome"):

    pred = model.predict(X)[0]

    conf = 0
    if hasattr(model, "predict_proba"):
        conf = model.predict_proba(X)[0].max() * 100

    st.divider()

    # -------------------------
    # RESULT DISPLAY
    # -------------------------
    if pred == 1:
        if conf >= 90:
            label = "🎬 BLOCKBUSTER"
            st.success(label)
            st.balloons()
            st.markdown("### 🔥 Industry Breakout Prediction")
        else:
            label = "🔥 HIT"
            st.success(label)
            st.markdown("### 📈 Strong Commercial Performance")
    else:
        if conf < 40:
            label = "💀 FLOP RISK"
            st.error(label)
            st.markdown("### ⚠️ High Financial Risk Detected")
        else:
            label = "⚖️ AVERAGE"
            st.warning(label)
            st.markdown("### 📊 Moderate Performance Expected")

    # -------------------------
    # METRICS
    # -------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.metric("🎯 Result", label)

    with col2:
        st.metric("📊 Confidence", f"{conf:.1f}%")

    st.progress(conf / 100)

    # -------------------------
    # INSIGHTS ENGINE
    # -------------------------
    st.markdown("## 🎥 Studio Insights (AI Analysis Layer)")

    if popularity < 40:
        st.write("• Low audience buzz detected")

    if budget > 20000000:
        st.write("• High production cost increases financial risk")

    if runtime > 180:
        st.write("• Long runtime may reduce audience retention")

    if genre == "Action":
        st.write("• Action films are competitive but high-reward genre")