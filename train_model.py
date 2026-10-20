"""
train_model.py - Training Script for PhishGuard Lite.
Uses pathlib so it can be executed from any working directory.
"""

from pathlib import Path
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from features import extract_features, FEATURE_NAMES

# Base directory of PhishGuard-Lite
BASE_DIR = Path(__file__).resolve().parent

def main():
    data_path = BASE_DIR / "data" / "urls.csv"
    print("=== Step 1: Loading Dataset ===")
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df):,} URLs from {data_path.name}")

    print("\n=== Step 2: Extracting 5 Features ===")
    feature_rows = [extract_features(url) for url in df["url"]]
    X = pd.DataFrame(feature_rows)[FEATURE_NAMES]
    y = df["label"]

    print("Sample feature matrix:")
    print(X.head())

    print("\n=== Step 3: Train / Test Split (80% Train, 20% Test) ===")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Training samples: {len(X_train):,}")
    print(f"Testing samples:  {len(X_test):,}")

    print("\n=== Step 4: Training Decision Tree Classifier ===")
    # max_depth=6 prevents overfitting and makes tree decisions easy to understand
    model = DecisionTreeClassifier(max_depth=6, random_state=42)
    model.fit(X_train, y_train)
    print("Model training complete!")

    print("\n=== Step 5: Evaluating Model on Test Set ===")
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print(f"Accuracy:  {acc * 100:.2f}%")
    print(f"Precision: {prec * 100:.2f}%")
    print(f"Recall:    {rec * 100:.2f}%")
    print(f"F1-Score:  {f1 * 100:.2f}%")
    print("\nConfusion Matrix:")
    print(f"  [TN: {cm[0,0]}  FP: {cm[0,1]}]")
    print(f"  [FN: {cm[1,0]}  TP: {cm[1,1]}]")

    print("\n=== Step 6: Saving Model Artifact ===")
    model_data = {
        "model": model,
        "feature_names": FEATURE_NAMES,
        "metrics": {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "cm": cm.tolist()
        }
    }
    model_save_path = BASE_DIR / "model.joblib"
    joblib.dump(model_data, model_save_path)
    print(f"Model saved successfully to '{model_save_path.name}'!")

if __name__ == "__main__":
    main()
