from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score, confusion_matrix
from sklearn.linear_model import LinearRegression, LogisticRegression
import joblib

ROOT = Path(__file__).resolve().parents[3]
FEAT_CSV = ROOT / "sdg_ea_pipeline" / "data" / "processed" / "fe" / "features.csv"
OUTPUT_MODELS_DIR = ROOT / "sdg_ea_pipeline" / "models"
REPORTS_DIR = ROOT / "sdg_ea_pipeline" / "data" / "processed" / "fe" / "model_reports"


def ensure_dirs():
    OUTPUT_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def load_features():
    if not FEAT_CSV.exists():
        raise FileNotFoundError(f"Features file not found at {FEAT_CSV}. Run STEP 5 first.")
    df = pd.read_csv(FEAT_CSV)
    return df


def prepare_dataset(df: pd.DataFrame):
    if 'target_value' in df.columns:
        y = df['target_value'].astype(float)
        X = df.drop(columns=['target_value'])
    elif 'value' in df.columns:
        y = df['value'].astype(float)
        X = df.drop(columns=['value'])
    else:
        raise ValueError("No target column found for regression: 'target_value' or 'value'.")

    X = X.select_dtypes(include=[np.number]).fillna(0)
    if 'country' in X.columns and 'indicator_code' in X.columns:
        X = pd.get_dummies(X, columns=["country", "indicator_code"], drop_first=True)
    y = y.astype(float)
    return X, y


def train_regression(X, y):
    if X.shape[0] < 2:
        raise ValueError("Not enough data to train regression.")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    reg = LinearRegression()
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse_np = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(rmse_np)
    r2 = r2_score(y_test, y_pred)
    return reg, X_test, y_test, y_pred, {'mae': mae, 'rmse': rmse, 'r2': r2}


def train_classification(X, y):
    if len(y) < 2:
        return None, None, None, None, {'skipped':'not_enough_data'}
    median = y.median()
    y_class = (y > median).astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y_class, test_size=0.2, random_state=42)
    clf = LogisticRegression(max_iter=1000, solver='liblinear')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    return clf, X_test, y_test, y_pred, {'accuracy': acc, 'confusion_matrix': cm.tolist()}


def main():
    ensure_dirs()
    df = load_features()
    X, y = prepare_dataset(df)

    reg_model, X_t, y_t, y_pred, reg_metrics = train_regression(X, y)
    joblib.dump(reg_model, str(OUTPUT_MODELS_DIR / 'linear_regression.joblib'))

    report = {
        'model': 'LinearRegression',
        'metrics': reg_metrics,
        'n_features': X.shape[1],
    }
    with open(REPORTS_DIR / 'regression_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    clf_model, X_t2, y_t2, y_pred2, clf_metrics = train_classification(X, y)
    if clf_model is not None:
        joblib.dump(clf_model, str(OUTPUT_MODELS_DIR / 'logistic_regression.joblib'))
        report_clf = {
            'model': 'LogisticRegression',
            'metrics': clf_metrics,
            'n_features': X.shape[1],
        }
        with open(REPORTS_DIR / 'classification_report.json', 'w', encoding='utf-8') as f:
            json.dump(report_clf, f, indent=2)
    print("STEP 6: Baseline models trained.")


if __name__ == '__main__':
    main()
