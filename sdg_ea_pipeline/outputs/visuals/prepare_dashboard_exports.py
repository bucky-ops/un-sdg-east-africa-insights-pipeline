from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
FEATS_PATH = ROOT / "sdg_ea_pipeline" / "data" / "processed" / "fe" / "features.csv"
DASH_OUTPUT_DIR = ROOT / "sdg_ea_pipeline" / "outputs" / "visuals"
DASHBOARD_CSV = DASH_OUTPUT_DIR / "dashboard_ready.csv"
DASHBOARD_META = DASH_OUTPUT_DIR / "dashboard_meta.json"


def main():
    DASH_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not FEATS_PATH.exists():
        raise FileNotFoundError(f"Features file not found at {FEATS_PATH}. Run STEP 5 first.")
    df = pd.read_csv(FEATS_PATH)
    # Build a compact dashboard-ready frame
    required = ["country", "indicator_code", "year", "value_filled", "yoy_change", "rolling_mean_3", "rolling_std_3", "risk_level"]
    exist_cols = [c for c in required if c in df.columns]
    df_out = df[exist_cols].copy()
    df_out.to_csv(DASHBOARD_CSV, index=False)

    meta = {
        "columns": exist_cols,
        "description": "Dashboard-ready export for BI tools. Columns map to policy indicators and recent trends.",
    }
    with open(DASHBOARD_META, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2)
    print(f"Dashboard exports written to {DASHBOARD_CSV}")

if __name__ == '__main__':
    main()
