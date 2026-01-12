from __future__ import annotations
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CLEANED_PATH = ROOT / "sdg_ea_pipeline" / "data" / "processed" / "cleaned.csv"
OUTPUT_DIR = ROOT / "sdg_ea_pipeline" / "data" / "processed" / "fe"
FEATURES_OUTPUT = OUTPUT_DIR / "features.csv"
FEATURES_LONG_OUTPUT = OUTPUT_DIR / "features_long.csv"


def load_cleaned() -> pd.DataFrame:
    if not CLEANED_PATH.exists():
        raise FileNotFoundError(f"Cleaned data not found at {CLEANED_PATH}. Run STEP 4 first.")
    df = pd.read_csv(CLEANED_PATH)
    # Normalize target column to a unified name
    if 'target_value' in df.columns:
        df = df.rename(columns={'target_value': 'target_value'})
    elif 'value' in df.columns:
        df = df.rename(columns={'value': 'target_value'})
    else:
        raise ValueError("No target column found (expected 'target_value' or 'value').")
    return df


def harmonize_input(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if 'country' in df.columns:
        df['country'] = df['country'].astype(str).str.upper()
    if 'indicator_code' in df.columns:
        df['indicator_code'] = df['indicator_code'].astype(str).str.upper()
    return df


def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(by=["country", "indicator_code", "year"]).copy()
    if 'target_value' not in df.columns:
        raise ValueError("Input dataframe must contain 'target_value' column.")
    # YoY change with grouping; safe for stable environments
    df['yoy_change'] = df.groupby(["country", "indicator_code"])["target_value"].transform(lambda s: s.pct_change()) * 100
    # Simple risk indicator: below mean => low, above mean => high
    mean_by_group = df.groupby(['indicator_code'])['target_value'].transform('mean')
    df['risk_level'] = (df['target_value'] > mean_by_group).map({True: 'high', False: 'low'})
    df['year'] = df['year'].astype('Int64')
    return df


def save_outputs(df: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(FEATURES_OUTPUT, index=False)
    long = df.copy()
    value_cols = ["target_value", "yoy_change"]
    available = [c for c in value_cols if c in long.columns]
    if available:
        long = long.melt(id_vars=["country", "indicator_code", "year"], value_vars=available,
                         var_name="feature", value_name="feature_value")
    long.to_csv(FEATURES_LONG_OUTPUT, index=False)


def main():
    df = load_cleaned()
    df = harmonize_input(df)
    df = compute_features(df)
    save_outputs(df)
    print(f"Features written: {FEATURES_OUTPUT} and {FEATURES_LONG_OUTPUT}")


if __name__ == "__main__":
    main()
