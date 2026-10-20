"""
PhishGuard Lite
Simple, minimalist phishing URL detector using a Decision Tree model.
"""

from pathlib import Path
import streamlit as st
import pandas as pd
import joblib

from features import extract_features, FEATURE_NAMES

# 1. Page Configuration
st.set_page_config(
    page_title="PhishGuard Lite",
    layout="centered"
)

# 2. Minimalist Styling
st.markdown("""
<style>
/* Clean typography & spacing */
.title-container {
    text-align: center;
    margin-top: 1rem;
    margin-bottom: 2rem;
}
.main-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 0.3rem;
}
.sub-title {
    font-size: 1rem;
    color: #94a3b8;
}
.result-card {
    padding: 1.25rem 1.5rem;
    border-radius: 8px;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
    text-align: center;
}
.result-phish {
    background-color: #450a0a;
    border: 1px solid #dc2626;
    color: #fee2e2;
}
.result-legit {
    background-color: #064e3b;
    border: 1px solid #10b981;
    color: #ecfdf5;
}
.result-header {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}
.result-sub {
    font-size: 0.95rem;
    opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)

# 3. Model Loading
BASE_DIR = Path(__file__).resolve().parent
model_path = BASE_DIR / "model.joblib"

@st.cache_resource
def load_model():
    if not model_path.exists():
        return None
    return joblib.load(model_path)

model_package = load_model()

# 4. Header (Ultra Clean, No Emojis)
st.markdown("""
<div class="title-container">
    <div class="main-title">PhishGuard Lite</div>
    <div class="sub-title">Simple Phishing URL Detection using Machine Learning</div>
</div>
""", unsafe_allow_html=True)

if model_package is None:
    st.error("Model file model.joblib not found. Please run train_model.py first.")
    st.stop()

model = model_package["model"]

# 5. Quick Test Buttons (Clean Text)
st.write("Test a sample URL or enter your own:")
col1, col2 = st.columns(2)
demo_url = ""

if col1.button("Phishing Sample", use_container_width=True):
    demo_url = "http://paypal-verification-account-update.xyz/login.php?account=123"

if col2.button("Legitimate Sample", use_container_width=True):
    demo_url = "https://www.wikipedia.org/wiki/Computer_science"

# 6. URL Input Form
user_input = st.text_input(
    label="Enter URL to scan:",
    value=demo_url,
    placeholder="e.g. http://mybank-login.com"
)

scan_clicked = st.button("Scan URL", type="primary", use_container_width=True)

# 7. Prediction & Output
if scan_clicked or demo_url:
    target_url = user_input.strip()
    if not target_url:
        st.warning("Please enter a URL to scan.")
    else:
        # Extract features
        features_dict = extract_features(target_url)
        df_features = pd.DataFrame([features_dict])[FEATURE_NAMES]

        # Model Prediction
        prediction = int(model.predict(df_features)[0])
        probabilities = model.predict_proba(df_features)[0]
        prob_phishing = float(probabilities[1]) * 100

        # Result Banner
        if prediction == 1:
            st.markdown(f"""
            <div class="result-card result-phish">
                <div class="result-header">Prediction: Potentially Phishing</div>
                <div class="result-sub">Risk Score: {prob_phishing:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-card result-legit">
                <div class="result-header">Prediction: Likely Legitimate</div>
                <div class="result-sub">Risk Score: {prob_phishing:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

        # Extracted Features Table
        with st.expander("Extracted Features", expanded=True):
            display_df = pd.DataFrame([
                {"Feature": "URL Length", "Value": str(features_dict["url_length"])},
                {"Feature": "Number of Dots", "Value": str(features_dict["num_dots"])},
                {"Feature": "Contains '@' Symbol", "Value": "Yes" if features_dict["has_at_symbol"] else "No"},
                {"Feature": "Hyphens in Hostname", "Value": str(features_dict["num_hyphens_hostname"])},
                {"Feature": "Uses HTTPS", "Value": "Yes" if features_dict["is_https"] else "No"},
            ])
            st.dataframe(display_df, hide_index=True, use_container_width=True)

        st.caption("Notice: This machine learning model evaluates lexical patterns only. A legitimate prediction is an estimate and does not guarantee complete safety.")
