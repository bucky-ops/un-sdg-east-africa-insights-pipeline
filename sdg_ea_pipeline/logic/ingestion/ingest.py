from __future__ import annotations
import os
from pathlib import Path
import shutil
from datetime import datetime
import logging
import pandas as pd

# Project root resolution (assumes standard repo layout)
ROOT = Path(__file__).resolve().parents[3]
PLACEHOLDERS_DIR = ROOT / "sdg_ea_pipeline" / "data" / "raw" / "placeholders"
ARCHIVE_DIR = ROOT / "sdg_ea_pipeline" / "data" / "raw" / "archive"
INTERIM_DIR = ROOT / "sdg_ea_pipeline" / "data" / "interim"
PROVENANCE_DIR = ROOT / "sdg_ea_pipeline" / "data" / "provenance"
PROVENANCE_FILE = PROVENANCE_DIR / "provenance.csv"
LOG_DIR = ROOT / "sdg_ea_pipeline" / "logs"
LOG_PATH = LOG_DIR / "ingestion.log" 

REQUIRED_COLUMNS = {"source", "year", "country", "indicator_code", "value", "reliability"}


def setup_logging(log_path: Path) -> None:
    log_dir = log_path.parent
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.FileHandler(str(log_path)), logging.StreamHandler()],
    )


def ensure_dirs() -> None:
    for d in [PLACEHOLDERS_DIR, ARCHIVE_DIR, INTERIM_DIR, PROVENANCE_DIR, LOG_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def ensure_dummy_placeholder() -> None:
    # Create a small example CSV if no placeholders exist yet
    PLACEHOLDERS_DIR.mkdir(parents=True, exist_ok=True)
    dummy_file = PLACEHOLDERS_DIR / "dummy_sdg.csv"
    if dummy_file.exists():
        return
    sample = [
        {"source": "UNSDG_placeholder", "year": 2020, "country": "KEN", "indicator_code": "I1", "value": 1000000, "reliability": "verified"},
        {"source": "UNSDG_placeholder", "year": 2021, "country": "KEN", "indicator_code": "I1", "value": 1010000, "reliability": "verified"},
        {"source": "UNSDG_placeholder", "year": 2020, "country": "UGA", "indicator_code": "I2", "value": 500000, "reliability": "estimated"},
        {"source": "UNSDG_placeholder", "year": 2021, "country": "UGA", "indicator_code": "I2", "value": 520000, "reliability": "estimated"},
        {"source": "UNSDG_placeholder", "year": 2022, "country": "TZA", "indicator_code": "I1", "value": 900000, "reliability": "verified"},
    ]
    df = pd.DataFrame(sample)
    dummy_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(dummy_file, index=False)
    logging.info(f"Created dummy placeholder at {dummy_file}")


def discover_placeholders() -> list[Path]:
    if not PLACEHOLDERS_DIR.exists():
        return []
    files = []
    for p in PLACEHOLDERS_DIR.glob("*"):
        if p.is_file() and p.suffix.lower() in {".csv", ".xlsx", ".xls"}:
            files.append(p)
    return sorted(files, key=lambda x: x.name)


def read_dataframe(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    elif path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported placeholder format: {path}")


def archive_source(path: Path) -> Path:
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archived = ARCHIVE_DIR / f"{path.stem}_{timestamp}{path.suffix}"
    shutil.copy2(str(path), str(archived))
    return archived


def write_interim(df: pd.DataFrame, original_path: Path) -> Path:
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    interim_path = INTERIM_DIR / f"ingested_{original_path.stem}_{timestamp}.csv"
    df.to_csv(interim_path, index=False)
    return interim_path


def append_provenance(record: dict) -> None:
    PROVENANCE_DIR.mkdir(parents=True, exist_ok=True)
    file_exists = PROVENANCE_FILE.exists()
    header = ["ingested_file", "source", "year_min", "year_max", "countries", "indicators", "status", "timestamp", "reliability_summary", "original_path"]
    with open(str(PROVENANCE_FILE), "a", encoding="utf-8", newline="") as f:
        writer = None
        import csv as _csv
        if not file_exists:
            writer = _csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
        else:
            writer = _csv.DictWriter(f, fieldnames=header)
        writer.writerow(record)


def ingest_file(path: Path) -> None:
    logging.info(f"Ingesting placeholder file: {path}")
    df = read_dataframe(path)
    # Archive raw source immutably
    archived = archive_source(path)
    # Write an interim, progression-friendly copy
    interim = write_interim(df, path)
    # Prepare provenance summary for this file
    year_vals = df["year"].astype(int) if "year" in df.columns else pd.Series(dtype=int)
    year_min = int(year_vals.min()) if not year_vals.empty else None
    year_max = int(year_vals.max()) if not year_vals.empty else None
    countries = ";".join(sorted(df["country"].astype(str).dropna().unique())) if "country" in df.columns else ""
    indicators = ";".join(sorted(df["indicator_code"].astype(str).dropna().unique())) if "indicator_code" in df.columns else ""
    reliability_summary = ";".join(sorted(df["reliability"].astype(str).dropna().unique())) if "reliability" in df.columns else ""
    provenance_record = {
        "ingested_file": interim.name,
        "source": str(df["source"].iloc[0]) if "source" in df.columns and not df["source"].empty else "",
        "year_min": year_min,
        "year_max": year_max,
        "countries": countries,
        "indicators": indicators,
        "status": "INGESTED",
        "timestamp": datetime.utcnow().isoformat(),
        "reliability_summary": reliability_summary,
        "original_path": str(path),
    }
    append_provenance(provenance_record)
    logging.info(
        f"Ingested {path.name}: archived -> {archived.name}, interim -> {interim.name}, provenance updated"
    )


def main() -> None:
    setup_logging(LOG_PATH)
    ensure_dirs()
    ensure_dummy_placeholder()
    placeholders = discover_placeholders()
    if not placeholders:
        logging.info("No placeholder files found in data/raw/placeholders.")
        return
    for p in placeholders:
        try:
            ingest_file(p)
        except Exception as e:
            logging.exception(f"Ingestion failed for {p}: {e}")


if __name__ == "__main__":
    main()
