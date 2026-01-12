from __future__ import annotations
import subprocess
import sys
from pathlib import Path

# End-to-end steps: 3 through 10 (STEP 3 is ingestion; STEP 4 cleaning; STEP 5 FE; STEP 6 baselines; STEP 7-10 validation, insights, visuals, deployment)
STEPS = [
    {
        "name": "Ingestion",
        "cmd": [sys.executable, str(Path(__file__).resolve().parents[0] / "logic" / "ingestion" / "ingest.py")],
    },
    {
        "name": "Cleaning",
        "cmd": [sys.executable, str(Path(__file__).resolve().parents[0] / "logic" / "cleaning" / "clean.py")],
    },
    {
        "name": "Feature Engineering",
        "cmd": [sys.executable, str(Path(__file__).resolve().parents[0] / "logic" / "fe" / "feature_engineering.py")],
    },
    {
        "name": "Baseline Models",
        "cmd": [sys.executable, str(Path(__file__).resolve().parents[0] / "logic" / "models" / "train_baseline.py")],
    },
    {
        "name": "Validation & Trust",
        "cmd": [sys.executable, str(Path(__file__).resolve().parents[0] / "logic" / "validation" / "validate.py")],
    },
    {
        "name": "Insights",
        "cmd": [sys.executable, str(Path(__file__).resolve().parents[0] / "outputs" / "insights" / "insight_generator.py")],
    },
    {
        "name": "Dashboard Exports",
        "cmd": [sys.executable, str(Path(__file__).resolve().parents[0] / "outputs" / "visuals" / "prepare_dashboard_exports.py")],
    },
    {
        "name": "Documentation & Deployment",
        "cmd": [sys.executable, str(Path(__file__).resolve().parents[0] / "deploy" / "documentation.py")],
    },
]


def run_step(step):
    name = step["name"]
    cmd = step["cmd"]
    print(f"[RUN] {name}: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] {name} failed with code {result.returncode}")
        print(result.stdout)
        print(result.stderr)
        sys.exit(result.returncode)
    else:
        print(f"[OK] {name} completed.")
        if result.stdout:
            print(result.stdout)


def main():
    root = Path(__file__).resolve().parents[0]
    print("Starting end-to-end pipeline (STEPS 3-10).")
    for step in STEPS:
        run_step(step)
    print("Pipeline complete. Outputs are in the sdg_ea_pipeline/ data/processed/ and models folders as described.")


if __name__ == "__main__":
    main()
