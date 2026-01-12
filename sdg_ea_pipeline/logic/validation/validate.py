from __future__ import annotations
import json
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FEAT_PATH = ROOT / 'sdg_ea_pipeline' / 'data' / 'processed' / 'fe' / 'features.csv'
VALIDATION_OUT = ROOT / 'sdg_ea_pipeline' / 'data' / 'processed' / 'fe' / 'validation_report.json'


def load_features():
    if not FEAT_PATH.exists():
        raise FileNotFoundError(f"Features file not found at {FEAT_PATH}. Run STEP 5 first.")
    return pd.read_csv(FEAT_PATH)


def main():
    df = load_features()
    # Build regression dataset locally
    if 'target_value' in df.columns:
        y = df['target_value'].astype(float)
        X = df.drop(columns=['target_value'])
    elif 'value' in df.columns:
        y = df['value'].astype(float)
        X = df.drop(columns=['value'])
    else:
        raise ValueError("No target column found for validation: 'target_value' or 'value'.")
    # Encode categoricals simply
    if 'country' in X.columns and 'indicator_code' in X.columns:
        X = pd.get_dummies(X, columns=["country", "indicator_code"], drop_first=True)
    X = X.select_dtypes(include=[np.number]).fillna(0)

    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    reg = LinearRegression()
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    try:
        rmse = mean_squared_error(y_test, y_pred, squared=False)
    except TypeError:
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    report = {
        'model': 'LinearRegression',
        'metrics': {'mae': float(mae), 'rmse': float(rmse), 'r2': float(r2)}
    }
    VALIDATION_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(VALIDATION_OUT, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print("Validation complete. Output:", VALIDATION_OUT)

if __name__ == '__main__':
    main()
