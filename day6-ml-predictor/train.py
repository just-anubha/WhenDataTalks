import streamlit as st
import pickle
import numpy as np

# -------------------------
# Load model + metadata
# -------------------------
MODEL_FILE = r'C:\Users\KIIT\Desktop\WHENDATATALKS\day6-ml-predictor\model.pkl'
META_FILE  = r'C:\Users\KIIT\Desktop\WHENDATATALKS\day6-ml-predictor\model_meta.pkl'

with open(MODEL_FILE, 'rb') as f:
    model = pickle.load(f)

with open(META_FILE, 'rb') as f:
    meta = pickle.load(f)

# -------------------------
# UI Setup
# -------------------------
st.set_page_config(page_title='CinePredict AI', page_icon='🎬', layout='centered')
st.title('🎬 CinePredict AI')
st.caption('Bollywood vs Hollywood — Hit or Flop Predictor')
st.divider()

# -------------------------
# Input Section
# -------------------------
col1, col2 = st.columns(2)

with col1:
    industry = st.selectbox('Industry', ['Bollywood', 'Hollywood'])
    genre = st.selectbox(
        'Genre',
        ['Action','Adventure','Animation','Drama','Horror','Romance','Science Fiction','Thriller','Family']
    )
    gross = st.number_input('Box office gross (crore INR)', min_value=1.0, value=500.0)

with col2:
    budget = st.number_input('Budget in USD', min_value=0.0, value=20000000.0, step=1000000.0)
    runtime = st.slider('Runtime (minutes)', 60, 240, 140)
    popularity = st.slider('Popularity score (0-100)', 0.0, 100.0, 50.0)
    month = st.selectbox(
        'Release month',
        list(range(1, 13)),
        format_func=lambda x: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][x-1]
    )

st.divider()

# -------------------------
# Prediction
# -------------------------
if st.button('🎬 Predict Hit or Flop', use_container_width=True, type='primary'):

    encoders = meta.get('encoders', {})

    # Safe encoding fallback
    ind_enc = encoders['industry'].transform([industry])[0] if 'industry' in encoders else 0
    genre_enc = encoders['genre'].transform([genre])[0] if 'genre' in encoders else 0

    # -------------------------
    # FEATURE ENGINEERING
    # -------------------------

    budget_inr = budget * 83

    profit = gross - budget_inr
    roi = gross / (budget_inr + 1e-6)   # avoid divide-by-zero

    # Runtime score (non-linear)
    if runtime < 80:
        runtime_score = 0.3
    elif runtime <= 150:
        runtime_score = 1.0
    elif runtime <= 180:
        runtime_score = 0.8
    else:
        runtime_score = 0.5

    # Month score
    month_score_map = {
        1:0.7, 2:0.6, 3:0.7, 4:0.8,
        5:0.9, 6:0.8, 7:1.0, 8:0.9,
        9:0.6, 10:0.7, 11:0.9, 12:1.0
    }
    month_score = month_score_map.get(month, 0.7)

    # -------------------------
    # Final feature vector
    # MUST match training order
    # -------------------------
    X = np.array([[
        ind_enc,
        genre_enc,
        gross,
        budget_inr,
        profit,
        roi,
        runtime_score,
        popularity,
        month_score
    ]])

    # -------------------------
    # Prediction
    # -------------------------
    pred = model.predict(X)[0]

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)[0]
        conf = float(np.max(proba)) * 100
    else:
        conf = 0.0

    # -------------------------
    # Output
    # -------------------------
    st.divider()

    if pred == 1:
        st.success('# 🎉 HIT!')
        st.balloons()
    else:
        st.error('# 💀 FLOP')

    st.metric('Confidence', f'{conf:.1f}%')
    st.progress(min(conf / 100, 1.0))

    # -------------------------
    # Engine insights
    # -------------------------
    st.divider()
    st.write("### 🧠 Engine Signals")

    st.write(f"ROI: {roi:.2f}")
    st.write(f"Profit (INR): ₹{profit:,.0f}")
    st.write(f"Runtime Score: {runtime_score}")
    st.write(f"Month Score: {month_score}")
    st.write(f"Popularity: {popularity}")

    # -------------------------
    # Feature importance
    # -------------------------
    with st.expander('📊 Feature importance'):
        importances = meta.get('importances', {})

        if importances:
            for feat, score in sorted(importances.items(), key=lambda x: -x[1]):
                st.write(f'**{feat}** — {score:.3f}')
                st.progress(float(score))
        else:
            st.info("Feature importance not available in metadata.")