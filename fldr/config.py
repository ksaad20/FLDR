"""Configuration management for FLDR."""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
import json
import os
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


DEFAULT_CONFIG_DIR = Path.home() / ".config" / "fldr"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.toml"


@dataclass(slots=True)
class GeneralConfig:
    """General application configuration."""

    project_name: str = "FLDR"
    log_level: str = "INFO"
    workspace: Path = Path.cwd()


@dataclass(slots=True)
class DetectionConfig:
    """Fault-line detection configuration."""

    enabled: bool = True
    confidence_threshold: float = 0.80
    max_fault_lines: int = 100
    enable_gpu: bool = False


@dataclass(slots=True)
class SensorConfig:
    """Sensor configuration."""

    lidar: bool = True
    camera: bool = True
    imu: bool = True
    gps: bool = True


@dataclass(slots=True)
class OutputConfig:
    """Output configuration."""

    output_directory: Path = Path("output")
    save_json: bool = True
    save_csv: bool = False
    save_images: bool = True


@dataclass(slots=True)
class FLDRConfig:
    """Top-level FLDR configuration."""

    general: GeneralConfig = field(default_factory=GeneralConfig)
    detection: DetectionConfig = field(default_factory=DetectionConfig)
    sensors: SensorConfig = field(default_factory=SensorConfig)
    output: OutputConfig = field(default_factory=OutputConfig)

    def validate(self) -> None:
        """Validate configuration values."""
        threshold = self.detection.confidence_threshold

        if not 0.0 <= threshold <= 1.0:
            msg = "confidence_threshold must be between 0 and 1."
            raise ValueError(msg)

        if self.detection.max_fault_lines < 1:
            msg = "max_fault_lines must be positive."
            raise ValueError(msg)


def default_config() -> FLDRConfig:
    """Return the default configuration."""
    return FLDRConfig()


def ensure_config_directory() -> Path:
    """Create the configuration directory if required."""
    DEFAULT_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    return DEFAULT_CONFIG_DIR


def load_environment(config: FLDRConfig) -> FLDRConfig:
    """Apply environment variable overrides."""
    log_level = os.getenv("FLDR_LOG_LEVEL")
    if log_level:
        config.general.log_level = log_level

    gpu = os.getenv("FLDR_ENABLE_GPU")
    if gpu:
        config.detection.enable_gpu = gpu.lower() in {
            "1",
            "true",
            "yes",
        }

    return config


def save_json(
    config: FLDRConfig,
    path: Path,
) -> None:
    """Save configuration as JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        json.dump(asdict(config), handle, indent=4, default=str)


def load_json(path: Path) -> FLDRConfig:
    """Load configuration from JSON."""
    with path.open("r", encoding="utf-8") as handle:
        data: dict[str, Any] = json.load(handle)

    config = default_config()

    _merge(config, data)

    config.validate()

    return config


def load_toml(path: Path) -> FLDRConfig:
    """Load configuration from TOML."""
    if tomllib is None:
        msg = "tomllib is unavailable."
        raise RuntimeError(msg)

    with path.open("rb") as handle:
        data: dict[str, Any] = tomllib.load(handle)

    config = default_config()

    _merge(config, data)

    config.validate()

    return config


def _merge(config: FLDRConfig, data: dict[str, Any]) -> None:
    """Merge user configuration into the defaults."""
    for section_name, values in data.items():
        section = getattr(config, section_name, None)

        if section is None or not isinstance(values, dict):
            continue

        for key, value in values.items():
            if hasattr(section, key):
                setattr(section, key, value)
