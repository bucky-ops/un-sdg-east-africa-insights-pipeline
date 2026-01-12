from __future__ import annotations
import os
from typing import Optional
from dataclasses import dataclass

try:
    import yaml  # PyYAML; optional if YAML config is used
    YAML_AVAILABLE = True
except Exception:
    YAML_AVAILABLE = False

# Fallback defaults imported from Python config
try:
    from .defaults import CONFIG as DEFAULT_CONFIG
except Exception:
    DEFAULT_CONFIG = {}

@dataclass
class GovernanceConfig:
    countries: list
    sdgs: list
    indicators: list
    years: list
    metadata_schema: dict
    data_quality_flags: dict

def _validate(cfg: GovernanceConfig) -> None:
    if not isinstance(cfg.countries, list) or not cfg.countries:
        raise ValueError("GovernanceConfig: 'countries' must be a non-empty list.")
    if not isinstance(cfg.sdgs, list) or not cfg.sdgs:
        raise ValueError("GovernanceConfig: 'sdgs' must be a non-empty list.")
    if not isinstance(cfg.indicators, list) or not cfg.indicators:
        raise ValueError("GovernanceConfig: 'indicators' must be a non-empty list.")
    if not isinstance(cfg.years, list) or not cfg.years:
        raise ValueError("GovernanceConfig: 'years' must be a non-empty list.")
    if not isinstance(cfg.metadata_schema, dict) or "fields" not in cfg.metadata_schema:
        raise ValueError("GovernanceConfig: 'metadata_schema' must contain 'fields'.")
    if not isinstance(cfg.data_quality_flags, dict):
        raise ValueError("GovernanceConfig: 'data_quality_flags' must be a dict.")

def load_config(config_path: Optional[str] = None) -> GovernanceConfig:
    data = None

    # Attempt YAML load if path provided and YAML library is available
    if config_path and os.path.exists(config_path) and YAML_AVAILABLE:
        with open(config_path, "r", encoding="utf-8") as f:
            payload = yaml.safe_load(f) or {}
            data = payload

    if data:
        cfg = GovernanceConfig(
            countries=data.get("countries", DEFAULT_CONFIG.get("countries", [])),
            sdgs=data.get("sdgs", DEFAULT_CONFIG.get("sdgs", [])),
            indicators=data.get("indicators", DEFAULT_CONFIG.get("indicators", [])),
            years=data.get("years", DEFAULT_CONFIG.get("years", [])),
            metadata_schema=data.get("metadata_schema", DEFAULT_CONFIG.get("metadata_schema", {})),
            data_quality_flags=data.get("data_quality_flags", DEFAULT_CONFIG.get("data_quality_flags", {})),
        )
    else:
        if isinstance(DEFAULT_CONFIG, dict) and DEFAULT_CONFIG:
            cfg = GovernanceConfig(
                countries=DEFAULT_CONFIG.get("countries", []),
                sdgs=DEFAULT_CONFIG.get("sdgs", []),
                indicators=DEFAULT_CONFIG.get("indicators", []),
                years=DEFAULT_CONFIG.get("years", []),
                metadata_schema=DEFAULT_CONFIG.get("metadata_schema", {}),
                data_quality_flags=DEFAULT_CONFIG.get("data_quality_flags", {}),
            )
        else:
            raise RuntimeError("GovernanceConfig: No configuration data available.")

    _validate(cfg)
    return cfg

__all__ = ["GovernanceConfig", "load_config"]
