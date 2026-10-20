# PhishGuard Lite 🛡️

A simple, beginner-friendly phishing URL detection system built with Python, scikit-learn, and Streamlit.

---

## 1. Project Overview & Scope
PhishGuard Lite is designed specifically for college submissions and viva voce defense:
- **Input**: A URL string typed by the user (e.g. `http://paypal-verification.com/login`).
- **Processing**: Extracts **5 simple, intuitive lexical features** from the URL string alone.
- **Classification**: Uses a single, transparent **Decision Tree Classifier** trained on 10,000 labeled URLs.
- **Output**: Predicts **Potentially Phishing** or **Likely Legitimate**, accompanied by an estimated risk percentage and feature breakdown.
- **Deliberate Scope Limit**: Strictly **zero network requests, DNS lookups, or HTML downloads**. All computation is 100% offline and safe.

---

## 2. The 5 Extracted Features
| # | Feature Name | Description | Why It Signals Phishing |
|---|---|---|---|
| 1 | `url_length` | Total number of characters | Phishing URLs often include long tokens and redirections |
| 2 | `num_dots` | Total count of dots (`.`) | Indicates deep subdomains or numerical IP host representations |
| 3 | `has_at_symbol` | Presence of `@` symbol (1/0) | The `@` symbol tricks browsers into ignoring text before it |
| 4 | `num_hyphens_hostname` | Hyphen count in hostname | Hyphens are frequently used to mimic brands (e.g. `paypal-secure`) |
| 5 | `is_https` | Uses `https://` (1/0) | Educational signal; lack of HTTPS is an indicator of unverified sites |

---

## 3. Project Structure
```
PhishGuard-Lite/
├── data/
│   └── urls.csv          # Clean dataset of 10,000 balanced URLs (5,000 Phishing, 5,000 Legitimate)
├── features.py           # Single source of truth for extracting the 5 features
├── train_model.py        # Loads data, trains Decision Tree, evaluates, saves model.joblib
├── app.py                # Simple Streamlit web interface
├── model.joblib          # Serialized Decision Tree model artifact
├── requirements.txt      # Minimal pinned dependencies
├── README.md             # This documentation
└── .gitignore            # Ignores virtual environment and temporary caches
```

---

## 4. Evaluation Results (Real Measured Numbers)
Evaluated on an untouched test set of 2,000 URLs (stratified 50/50):
- **Accuracy**: 63.20%
- **Precision**: 76.61%
- **Recall**: 38.00%
- **F1-Score**: 50.80%

*Note for Viva*: A simple 5-feature Decision Tree offers clear interpretability. Precision is high (76.6%), meaning when the model alerts phishing, it is correct over three-quarters of the time, while keeping the decision logic completely readable for examiners.

---

## 5. Quickstart & How to Run

### Step 1: Activate Virtual Environment
```powershell
cd PhishGuard-Lite
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Train the Model (Generates `model.joblib`)
```powershell
python train_model.py
```

### Step 4: Run the Web Dashboard
```powershell
streamlit run app.py
```
Open your browser at: **`http://localhost:8502`**

---

## 6. Disclaimer
This machine learning system evaluates string-level lexical indicators only. A "Likely Legitimate" result is an educational estimate and does not guarantee that a website is safe. Never enter credentials on untrusted websites.
