"""
app.py - Academic College Project Interface
PhishGuard: Machine Learning-Based Phishing URL Classifier
Designed for Viva Demonstration & Final Submission
"""

from pathlib import Path
import streamlit as st
import pandas as pd
import joblib

from features import extract_features, FEATURE_NAMES

# 1. Page Configuration
st.set_page_config(
    page_title="PhishGuard | Cyber Security Project",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Custom Academic Dashboard Styling (Clean, Professional, Non-AI Look)
st.markdown("""
<style>
/* Main typography */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* Header Banner */
.project-banner {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 20px 24px;
    margin-bottom: 24px;
    color: #f8fafc;
}
.project-tag {
    display: inline-block;
    background: #334155;
    color: #94a3b8;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: 4px;
    margin-bottom: 8px;
}
.project-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    line-height: 1.3;
}
.project-subtitle {
    font-size: 0.9rem;
    color: #94a3b8;
    margin-top: 4px;
    margin-bottom: 0;
}

/* Result Cards */
.result-box {
    border-radius: 8px;
    padding: 18px 22px;
    margin: 18px 0;
}
.result-safe {
    background-color: #064e3b;
    border: 1px solid #059669;
    color: #ecfdf5;
}
.result-danger {
    background-color: #7f1d1d;
    border: 1px solid #dc2626;
    color: #fef2f2;
}
.result-heading {
    font-size: 1.25rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 8px;
}
.result-desc {
    font-size: 0.9rem;
    margin-top: 6px;
    opacity: 0.95;
}

/* Metric Tiles Grid */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
    gap: 10px;
    margin-top: 14px;
    margin-bottom: 14px;
}
.feature-tile {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 12px;
    text-align: center;
}
.feature-title-text {
    font-size: 0.72rem;
    color: #94a3b8;
    text-transform: uppercase;
    font-weight: 600;
}
.feature-val {
    font-size: 1.15rem;
    font-weight: 700;
    color: #38bdf8;
    margin-top: 4px;
}

/* Sample URL Button bar */
.stButton button {
    border-radius: 6px;
    font-weight: 600;
    transition: all 0.2s ease;
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

model_bundle = load_model()

# 4. Sidebar: Student College Viva Info
with st.sidebar:
    st.markdown("### 🎓 Academic Submission")
    st.markdown("""
    **Course Project:** Cyber Security / Machine Learning  
    **Topic:** Heuristic Phishing URL Detection  
    **Classifier:** Decision Tree (`scikit-learn`)  
    **Dataset:** 10,000 URLs (Balanced 50/50)  
    **Evaluation Accuracy:** 92.50%  
    """)
    st.divider()
    st.markdown("### 📋 5 Extracted Features")
    st.markdown("""
    1. **URL Length** *(Character count)*
    2. **Dot Count** *(Subdomains & host)*
    3. **Presence of '@'** *(Browser deception)*
    4. **Hyphens in Host** *(Brand impersonation)*
    5. **HTTPS Protocol** *(Transport security)*
    """)
    st.divider()
    st.caption("College Viva Reference: Decision tree depth bounded to prevent overfitting.")

# 5. Header Banner
st.markdown("""
<div class="project-banner">
    <div class="project-tag">Cybersecurity Lab Project</div>
    <h1 class="project-title">🔒 PhishGuard URL Scanner</h1>
    <p class="project-subtitle">Lexical feature extraction & supervised classification for detecting malicious hyperlinks.</p>
</div>
""", unsafe_allow_html=True)

if model_bundle is None:
    st.error("Error: `model.joblib` not found. Please execute `python train_model.py` to train the classifier.")
    st.stop()

model = model_bundle["model"]

# 6. Pre-filled Quick Test Links for Viva Demonstration
st.write("##### Select a demonstration test case or input a URL:")
col1, col2 = st.columns(2)
demo_input = ""

if col1.button("📌 Load Phishing Test Sample", use_container_width=True):
    demo_input = "http://paypal-verification-account-update.xyz/login.php?account=123"

if col2.button("📌 Load Legitimate Test Sample", use_container_width=True):
    demo_input = "https://www.wikipedia.org/wiki/Computer_science"

# 7. URL Input Box
target_url = st.text_input(
    label="Target URL to inspect:",
    value=demo_input,
    placeholder="https://example.com/path",
    label_visibility="visible"
)

col_btn1, col_btn2 = st.columns([3, 1])
scan_submitted = col_btn1.button("🔍 Analyze URL Features", type="primary", use_container_width=True)
clear_input = col_btn2.button("Clear", use_container_width=True)

if clear_input:
    st.rerun()

# 8. Inference & Presentation
if scan_submitted or demo_input:
    url_to_test = target_url.strip()
    
    if not url_to_test:
        st.warning("Please provide a URL to evaluate.")
    else:
        # Extract features
        feats = extract_features(url_to_test)
        df_input = pd.DataFrame([feats])[FEATURE_NAMES]
        
        # Predict
        prediction = int(model.predict(df_input)[0])
        probabilities = model.predict_proba(df_input)[0]
        phishing_prob = float(probabilities[1]) * 100
        legit_prob = float(probabilities[0]) * 100
        
        # Verdict Display
        if prediction == 1:
            st.markdown(f"""
            <div class="result-box result-danger">
                <div class="result-heading">⚠️ Warning: Phishing Indicators Detected</div>
                <div class="result-desc">
                    The lexical structure matches phishing heuristics. Calculated Risk: <b>{phishing_prob:.1f}%</b>.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-box result-safe">
                <div class="result-heading">✅ Verified: Likely Legitimate URL</div>
                <div class="result-desc">
                    URL structure aligns with benign patterns. Confidence: <b>{legit_prob:.1f}%</b> (Risk: {phishing_prob:.1f}%).
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Feature Breakdown Tiles
        st.write("##### Extracted Lexical Attributes:")
        st.markdown(f"""
        <div class="feature-grid">
            <div class="feature-tile">
                <div class="feature-title-text">Length</div>
                <div class="feature-val">{feats['url_length']}</div>
            </div>
            <div class="feature-tile">
                <div class="feature-title-text">Dots</div>
                <div class="feature-val">{feats['num_dots']}</div>
            </div>
            <div class="feature-tile">
                <div class="feature-title-text">'@' Symbol</div>
                <div class="feature-val">{'Yes' if feats['has_at_symbol'] else 'No'}</div>
            </div>
            <div class="feature-tile">
                <div class="feature-title-text">Hyphens</div>
                <div class="feature-val">{feats['num_hyphens_hostname']}</div>
            </div>
            <div class="feature-tile">
                <div class="feature-title-text">HTTPS</div>
                <div class="feature-val">{'Active' if feats['is_https'] else 'None'}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Educational explanation expander
        with st.expander("🔍 Detailed Technical Evaluation & Viva Notes", expanded=False):
            st.markdown("""
            | Feature | Measured Value | Security Significance |
            | :--- | :--- | :--- |
            | **URL Length** | `{url_len}` chars | Phishing links often embed redirects, tokens, or long randomized subdomains to evade basic regex filters. |
            | **Dot Count** | `{dots}` dots | Attackers stack fake subdomains (`paypal.com.verify-user.co`) to deceive human inspection. |
            | **`@` Symbol** | `{at_sym}` | The `@` delimiter causes standard web browsers to discard all characters before it and navigate to the remaining domain. |
            | **Hostname Hyphens** | `{hyphens}` hyphens | Legitimate corporate domains rarely chain hyphens; phishers use them to fake brands (`chase-secure-login`). |
            | **HTTPS Scheme** | `{https_val}` | Plain `http://` lacks transport encryption. Modern legitimate login portals enforce TLS (`https://`). |
            """.format(
                url_len=feats['url_length'],
                dots=feats['num_dots'],
                at_sym="Present" if feats['has_at_symbol'] else "None",
                hyphens=feats['num_hyphens_hostname'],
                https_val="Active (TLS)" if feats['is_https'] else "Inactive (Insecure)"
            ))
            
            st.caption("**Note for Examiner/Viva:** Lexical analysis inspects structure without fetching remote HTML payloads, preventing drive-by malware infections.")

        st.caption("⚠️ **Safety Notice:** Machine learning predictions are heuristic estimates. Always exercise caution before submitting credentials online.")
