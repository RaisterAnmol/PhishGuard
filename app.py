"""
app.py - Minimal, Clean Web Application for PhishGuard Lite.
1. Accepts typed URL
2. Extracts the exact 5 features
3. Predicts using the saved Decision Tree model
4. Displays "Potentially Phishing" or "Likely Legitimate"
5. Displays extracted features and college safety disclaimer
"""

from pathlib import Path
import streamlit as st
import pandas as pd
import joblib

from features import extract_features, FEATURE_NAMES

# 1. Page Configuration
st.set_page_config(
    page_title="PhishGuard Lite",
    page_icon="🛡️",
    layout="centered"
)

# 2. Styling (Crisp, High-Contrast in Light and Dark Mode)
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}
.sub-title {
    text-align: center;
    font-size: 1.05rem;
    color: #6b7280;
    margin-bottom: 1.5rem;
}
.card {
    padding: 1.5rem;
    border-radius: 10px;
    text-align: center;
    margin-top: 1.2rem;
    margin-bottom: 1.2rem;
    font-size: 1.3rem;
    font-weight: bold;
}
.card-safe {
    background-color: #065f46;
    color: #ffffff;
    border: 2px solid #10b981;
}
.card-phish {
    background-color: #991b1b;
    color: #ffffff;
    border: 2px solid #ef4444;
}
</style>
""", unsafe_allow_html=True)

# 3. Load Model Artifact
BASE_DIR = Path(__file__).resolve().parent
model_path = BASE_DIR / "model.joblib"

@st.cache_resource
def load_saved_model():
    if not model_path.exists():
        return None
    return joblib.load(model_path)

model_package = load_saved_model()

# 4. Header
st.markdown('<div class="main-title">🛡️ PhishGuard Lite</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Simple Phishing URL Detection using Machine Learning</div>', unsafe_allow_html=True)

if model_package is None:
    st.error("⚠️ Model file `model.joblib` not found! Please run `python train_model.py` first.")
    st.stop()

model = model_package["model"]

# 5. Quick One-Click Samples for Easy Viva Demo
st.write("👉 **Test a sample URL or enter your own:**")
c1, c2 = st.columns(2)
demo_url = ""
if c1.button("🔴 Phishing Sample", use_container_width=True):
    demo_url = "http://paypal-verification-account-update.xyz/login.php?account=123"
if c2.button("🟢 Legitimate Sample", use_container_width=True):
    demo_url = "https://www.wikipedia.org/wiki/Computer_science"

# 6. URL Input Form
user_input = st.text_input("Enter URL to scan:", value=demo_url, placeholder="e.g. http://mybank-login.com")
scan_clicked = st.button("🔍 Scan URL", type="primary", use_container_width=True)

# 7. Prediction & Output
if scan_clicked or demo_url:
    cleaned_url = user_input.strip()
    if not cleaned_url:
        st.warning("Please type or paste a URL first.")
    else:
        # Step A: Extract exact 5 features
        features_dict = extract_features(cleaned_url)
        df_features = pd.DataFrame([features_dict])[FEATURE_NAMES]

        # Step B: Model Prediction
        prediction = int(model.predict(df_features)[0])
        # Decision tree probabilities: [prob_legit, prob_phish]
        prob_phish = float(model.predict_proba(df_features)[0][1])

        # Step C: Show Clean Result Card
        if prediction == 1:
            st.markdown(f"""
            <div class="card card-phish">
                🚨 Prediction: Potentially Phishing
                <div style="font-size: 1rem; font-weight: normal; margin-top: 6px;">
                    Estimated Phishing Risk: <b>{prob_phish * 100:.1f}%</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="card card-safe">
                ✅ Prediction: Likely Legitimate
                <div style="font-size: 1rem; font-weight: normal; margin-top: 6px;">
                    Estimated Phishing Risk: <b>{prob_phish * 100:.1f}%</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Step D: Show Extracted 5 Features Table (Great for Viva Explanation)
        with st.expander("📊 Extracted Features for this URL", expanded=True):
            display_df = pd.DataFrame([
                {"Feature": "1. Total URL Length", "Value": features_dict["url_length"], "Explanation": "Long URLs often hide malicious tokens"},
                {"Feature": "2. Dot Count", "Value": features_dict["num_dots"], "Explanation": "Excessive dots indicate subdomains or IP addresses"},
                {"Feature": "3. Has '@' Symbol", "Value": "Yes" if features_dict["has_at_symbol"] else "No", "Explanation": "'@' tricks browsers to ignore preceding text"},
                {"Feature": "4. Hostname Hyphens", "Value": features_dict["num_hyphens_hostname"], "Explanation": "Hyphens are used to mimic brand names (e.g. paypal-update)"},
                {"Feature": "5. Uses HTTPS", "Value": "Yes" if features_dict["is_https"] else "No", "Explanation": "1 if secure scheme, 0 if plain HTTP"},
            ])
            st.dataframe(display_df, hide_index=True, use_container_width=True)

        # Step E: Disclaimer
        st.info("ℹ️ **Notice:** This assessment is generated purely by extracting lexical features from the URL string. A 'Likely Legitimate' result is an educational estimate and does not guarantee that a website is safe.")

