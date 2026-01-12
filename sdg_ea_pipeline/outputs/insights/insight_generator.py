from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
FEATS_PATH = ROOT / "sdg_ea_pipeline" / "data" / "processed" / "fe" / "features.csv"
OUTPUT_DIR = ROOT / "sdg_ea_pipeline" / "outputs" / "insights"
INSIGHTS_TXT = OUTPUT_DIR / "insights.txt"
INSIGHTS_CSV = OUTPUT_DIR / "insights.csv"


def load_features():
    if not FEATS_PATH.exists():
        raise FileNotFoundError(f"Features file not found at {FEATS_PATH}. Run STEP 5 first.")
    return pd.read_csv(FEATS_PATH)


def generate_text_insights(df: pd.DataFrame) -> list:
    lines = []
    if 'country' in df.columns and 'indicator_code' in df.columns and 'yoy_change' in df.columns:
        grp = df.dropna(subset=['yoy_change']).groupby(['country','indicator_code'])['yoy_change'].mean().reset_index()
        top = grp.sort_values('yoy_change', ascending=False).head(3)
        parts = [f"{r['country']} {r['indicator_code']}: {r['yoy_change']:.1f}%" for _, r in top.iterrows()]
        lines.append("Top growing indicators: " + ", ".join(parts))
    if 'risk_level' in df.columns:
        high = df[df['risk_level'] == 'high']
        if not high.empty:
            c = high.groupby(['country','indicator_code']).size().reset_index(name='count')
            top = c.sort_values('count', ascending=False).head(3)
            parts = [f"{row['country']} {row['indicator_code']}" for _, row in top.iterrows()]
            lines.append("High risk observations: " + ", ".join(parts))
    if not lines:
        lines.append("No significant trends detected.")
    return lines


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_features()
    lines = generate_text_insights(df)
    with open(INSIGHTS_TXT, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    df[['country','indicator_code','year','yoy_change','risk_level']].to_csv(INSIGHTS_CSV, index=False)
    print(f"Insights generated: {INSIGHTS_TXT}")

if __name__ == '__main__':
    main()
