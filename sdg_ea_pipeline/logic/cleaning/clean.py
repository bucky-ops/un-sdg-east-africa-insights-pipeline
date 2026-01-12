import pandas as pd
import numpy as np
import glob
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INTERIM_DIR = ROOT / 'sdg_ea_pipeline' / 'data' / 'interim'
CLEANED_OUTPUT = ROOT / 'sdg_ea_pipeline' / 'data' / 'processed' / 'cleaned.csv'


def load_interims():
    interim_files = sorted(Path(INTERIM_DIR).glob('**/*.csv'))
    dfs = []
    for p in interim_files:
        try:
            df = pd.read_csv(p)
            dfs.append(df)
        except Exception:
            continue
    if not dfs:
        raise FileNotFoundError('No interim CSV files found for cleaning.')
    return pd.concat(dfs, ignore_index=True, sort=False)


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Ensure key columns exist
    if 'year' not in df.columns:
        df['year'] = pd.NA
    if 'country' not in df.columns:
        df['country'] = pd.NA
    if 'indicator_code' not in df.columns:
        df['indicator_code'] = pd.NA
    # Target value column
    if 'target_value' in df.columns:
        df['target_value'] = df['target_value']
    elif 'value' in df.columns:
        df['target_value'] = df['value']
    else:
        df['target_value'] = pd.NA
    # Simple numeric coercion
    df['target_value'] = pd.to_numeric(df['target_value'], errors='coerce')
    return df


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize(df)
    # Impute missing target with simple mean per indicator if possible
    if 'indicator_code' in df.columns and 'target_value' in df.columns:
        means = df.groupby('indicator_code')['target_value'].transform('mean')
        df['target_value'] = df['target_value'].fillna(means)
    # Ensure minimal required structure
    df = df.fillna({'country':'UNKNOWN', 'indicator_code':'UNKNOWN', 'year': df['year'].min() if 'year' in df else 0})
    # Output a cleaned copy
    df.to_csv(CLEANED_OUTPUT, index=False)
    return df


def main():
    df = load_interims()
    df_clean = clean_dataframe(df)
    print(f"Cleaned data written to {CLEANED_OUTPUT}")

if __name__ == '__main__':
    main()
