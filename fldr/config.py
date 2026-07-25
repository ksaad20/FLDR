"""
FLDR configuration management.

This module provides a centralized configuration system for the FLDR
framework. Configuration may originate from defaults, TOML files,
environment variables, or future plugin providers.
"""

from __future__ import annotations

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


__all__ = [
    "DEFAULT_CONFIG_DIRECTORY",
    "DEFAULT_CONFIG_FILE",
    "ConfigurationError",
    "GeneralConfig",
    "LoggingConfig",
    "SensorConfig",
    "DetectionConfig",
    "OutputConfig",
    "FLDRConfig",
    "create_default_config",
]


DEFAULT_CONFIG_DIRECTORY = Path.home() / ".config" / "fldr"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIRECTORY / "config.toml"


class ConfigurationError(ValueError):
    """Raised when a configuration file is invalid."""


@dataclass(slots=True)
class GeneralConfig:
    """General FLDR configuration."""

    application_name: str = "FLDR"
    version: str = "0.0.1"
    workspace: Path = Path.cwd()
    cache_directory: Path = Path.home() / ".cache" / "fldr"
    temporary_directory: Path = Path.cwd() / "tmp"


@dataclass(slots=True)
class LoggingConfig:
    """Logging configuration."""

    enabled: bool = True
    level: str = "INFO"
    log_directory: Path = Path.cwd() / "logs"
    log_filename: str = "fldr.log"
    console: bool = True
    file: bool = True


@dataclass(slots=True)
class SensorConfig:
    """Sensor configuration."""

    lidar: bool = True
    camera: bool = True
    imu: bool = True
    gps: bool = True
    wheel_encoder: bool = False
    radar: bool = False

    sampling_frequency_hz: float = 30.0

    enable_calibration: bool = True
    calibration_directory: Path = Path.cwd() / "calibration"


@dataclass(slots=True)
class DetectionConfig:
    """Fault-line detection configuration."""

    enabled: bool = True

    confidence_threshold: float = 0.80

    minimum_fault_length_m: float = 0.20

    maximum_fault_length_m: float = 1000.0

    maximum_faults: int = 100

    enable_gpu: bool = False

    enable_parallel_processing: bool = True


@dataclass(slots=True)
class OutputConfig:
    """Output configuration."""

    directory: Path = Path.cwd() / "output"

    save_json: bool = True

    save_csv: bool = True

    save_images: bool = True

    save_point_clouds: bool = True

    overwrite_existing: bool = False


@dataclass(slots=True)
class FLDRConfig:
    """Top-level FLDR configuration."""

    general: GeneralConfig = field(default_factory=GeneralConfig)

    logging: LoggingConfig = field(default_factory=LoggingConfig)

    sensors: SensorConfig = field(default_factory=SensorConfig)

    detection: DetectionConfig = field(default_factory=DetectionConfig)

    output: OutputConfig = field(default_factory=OutputConfig)

    def validate(self) -> None:
        """Validate the current configuration."""

        threshold = self.detection.confidence_threshold

        if not 0.0 <= threshold <= 1.0:
            msg = (
                "Detection confidence_threshold must "
                "be between 0.0 and 1.0."
            )
            raise ConfigurationError(msg)

        if self.detection.maximum_faults < 1:
            msg = "maximum_faults must be at least one."
            raise ConfigurationError(msg)

        if (
            self.detection.minimum_fault_length_m
            > self.detection.maximum_fault_length_m
        ):
            msg = (
                "minimum_fault_length_m cannot exceed "
                "maximum_fault_length_m."
            )
            raise ConfigurationError(msg)


def create_default_config() -> FLDRConfig:
    """Create a validated default configuration."""

    config = FLDRConfig()

    config.validate()

    def create_default_config() -> FLDRConfig:
    """Create a validated default configuration."""

    config = FLDRConfig()

    config.validate()

    return config


def ensure_config_directory() -> Path:
    """Create the default configuration directory if necessary."""

    DEFAULT_CONFIG_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    return DEFAULT_CONFIG_DIRECTORY

def config_exists() -> bool:
    """Return whether the default configuration file exists."""

    return DEFAULT_CONFIG_FILE.exists()


def load_environment(
    config: FLDRConfig,
) -> FLDRConfig:
    """Load configuration values from environment variables."""

    log_level = os.getenv("FLDR_LOG_LEVEL")

    if log_level is not None:
        config.logging.level = log_level.upper()

    enable_gpu = os.getenv("FLDR_ENABLE_GPU")

    if enable_gpu is not None:
        config.detection.enable_gpu = enable_gpu.lower() in {
            "1",
            "true",
            "yes",
            "on",
        }

    confidence = os.getenv(
        "FLDR_CONFIDENCE_THRESHOLD",
    )

    if confidence is not None:
        config.detection.confidence_threshold = float(
            confidence,
        )

    output_directory = os.getenv(
        "FLDR_OUTPUT_DIRECTORY",
    )

    if output_directory is not None:
        config.output.directory = Path(
            output_directory,
        )

    workspace = os.getenv(
        "FLDR_WORKSPACE",
    )

    if workspace is not None:
        config.general.workspace = Path(
            workspace,
        )

    config.validate()

    return config


def config_to_dict(
    config: FLDRConfig,
) -> dict[str, Any]:
    """Convert a configuration into a serializable dictionary."""

    return {
        "general": {
            "application_name": config.general.application_name,
            "version": config.general.version,
            "workspace": str(config.general.workspace),
            "cache_directory": str(
                config.general.cache_directory,
            ),
            "temporary_directory": str(
                config.general.temporary_directory,
            ),
        },
        "logging": {
            "enabled": config.logging.enabled,
            "level": config.logging.level,
            "log_directory": str(
                config.logging.log_directory,
            ),
            "log_filename": config.logging.log_filename,
            "console": config.logging.console,
            "file": config.logging.file,
        },
        "sensors": {
            "lidar": config.sensors.lidar,
            "camera": config.sensors.camera,
            "imu": config.sensors.imu,
            "gps": config.sensors.gps,
            "wheel_encoder": config.sensors.wheel_encoder,
            "radar": config.sensors.radar,
            "sampling_frequency_hz": (
                config.sensors.sampling_frequency_hz
            ),
            "enable_calibration": (
                config.sensors.enable_calibration
            ),
            "calibration_directory": str(
                config.sensors.calibration_directory,
            ),
        },
        "detection": {
            "enabled": config.detection.enabled,
            "confidence_threshold": (
                config.detection.confidence_threshold
            ),
            "minimum_fault_length_m": (
                config.detection.minimum_fault_length_m
            ),
            "maximum_fault_length_m": (
                config.detection.maximum_fault_length_m
            ),
            "maximum_faults": (
                config.detection.maximum_faults
            ),
            "enable_gpu": (
                config.detection.enable_gpu
            ),
            "enable_parallel_processing": (
                config.detection.enable_parallel_processing
            ),
        },
        "output": {
            "directory": str(
                config.output.directory,
            ),
            "save_json": config.output.save_json,
            "save_csv": config.output.save_csv,
            "save_images": config.output.save_images,
            "save_point_clouds": (
                config.output.save_point_clouds
            ),
            "overwrite_existing": (
                config.output.overwrite_existing
            ),
        },
    }
    def save_json(
    config: FLDRConfig,
    path: Path,
) -> None:
    """Save a configuration to a JSON file."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = config_to_dict(config)

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            sort_keys=True,
        )


def load_json(
    path: Path,
) -> FLDRConfig:
    """Load a configuration from a JSON file."""

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data: dict[str, Any] = json.load(file)

    config = create_default_config()

    general = data.get("general", {})

    config.general.application_name = general.get(
        "application_name",
        config.general.application_name,
    )

    config.general.version = general.get(
        "version",
        config.general.version,
    )

    config.general.workspace = Path(
        general.get(
            "workspace",
            str(config.general.workspace),
        ),
    )

    logging = data.get("logging", {})

    config.logging.enabled = logging.get(
        "enabled",
        config.logging.enabled,
    )

    config.logging.level = logging.get(
        "level",
        config.logging.level,
    )

    detection = data.get(
        "detection",
        {},
    )

    config.detection.enabled = detection.get(
        "enabled",
        config.detection.enabled,
    )

    config.detection.confidence_threshold = (
        detection.get(
            "confidence_threshold",
            config.detection.confidence_threshold,
        )
    )

    config.detection.maximum_faults = (
        detection.get(
            "maximum_faults",
            config.detection.maximum_faults,
        )
    )

    output = data.get(
        "output",
        {},
    )

    config.output.directory = Path(
        output.get(
            "directory",
            str(config.output.directory),
        ),
    )

    config.output.save_json = output.get(
        "save_json",
        config.output.save_json,
    )

    config.output.save_csv = output.get(
        "save_csv",
        config.output.save_csv,
    )

    config.output.save_images = output.get(
        "save_images",
        config.output.save_images,
    )

    config.validate()

    return config
    def load_toml(
    path: Path,
) -> FLDRConfig:
    """Load a configuration from a TOML file."""

    if tomllib is None:
        msg = "tomllib is unavailable on this Python version."
        raise ConfigurationError(msg)

    with path.open("rb") as file:
        data: dict[str, Any] = tomllib.load(file)

    config = create_default_config()

    general = data.get("general", {})

    config.general.application_name = general.get(
        "application_name",
        config.general.application_name,
    )

    config.general.version = general.get(
        "version",
        config.general.version,
    )

    config.general.workspace = Path(
        general.get(
            "workspace",
            str(config.general.workspace),
        ),
    )

    logging = data.get("logging", {})

    config.logging.enabled = logging.get(
        "enabled",
        config.logging.enabled,
    )

    config.logging.level = logging.get(
        "level",
        config.logging.level,
    )

    sensors = data.get("sensors", {})

    config.sensors.lidar = sensors.get(
        "lidar",
        config.sensors.lidar,
    )

    config.sensors.camera = sensors.get(
        "camera",
        config.sensors.camera,
    )

    config.sensors.imu = sensors.get(
        "imu",
        config.sensors.imu,
    )

    config.sensors.gps = sensors.get(
        "gps",
        config.sensors.gps,
    )

    detection = data.get(
        "detection",
        {},
    )

    config.detection.enabled = detection.get(
        "enabled",
        config.detection.enabled,
    )

    config.detection.confidence_threshold = detection.get(
        "confidence_threshold",
        config.detection.confidence_threshold,
    )

    config.detection.maximum_faults = detection.get(
        "maximum_faults",
        config.detection.maximum_faults,
    )

    output = data.get("output", {})

    config.output.directory = Path(
        output.get(
            "directory",
            str(config.output.directory),
        ),
    )

    config.output.save_json = output.get(
        "save_json",
        config.output.save_json,
    )

    config.output.save_csv = output.get(
        "save_csv",
        config.output.save_csv,
    )

    config.output.save_images = output.get(
        "save_images",
        config.output.save_images,
    )

    config.validate()

    return config


def discover_configuration() -> Path | None:
    """Discover the most appropriate configuration file."""

    candidates = (
        Path.cwd() / "fldr.toml",
        DEFAULT_CONFIG_FILE,
    )

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return None


def load_configuration() -> FLDRConfig:
    """Load the best available configuration."""

    config = create_default_config()

    path = discover_configuration()

    if path is None:
        return load_environment(config)

    if path.suffix == ".json":
        config = load_json(path)
    elif path.suffix == ".toml":
        config = load_toml(path)

    return load_environment(config)
    def save_default_configuration() -> Path:
    """Create the default configuration file if it does not exist."""

    ensure_config_directory()

    config = create_default_config()

    save_json(
        config,
        DEFAULT_CONFIG_FILE.with_suffix(".json"),
    )

    return DEFAULT_CONFIG_FILE.with_suffix(".json")


def reset_configuration() -> FLDRConfig:
    """Reset the configuration to its default values."""

    return create_default_config()


def configuration_summary(
    config: FLDRConfig,
) -> str:
    """Return a human-readable configuration summary."""

    lines = [
        "FLDR Configuration",
        "==================",
        "",
        "[General]",
        f"Application : {config.general.application_name}",
        f"Version     : {config.general.version}",
        f"Workspace   : {config.general.workspace}",
        "",
        "[Logging]",
        f"Enabled     : {config.logging.enabled}",
        f"Level       : {config.logging.level}",
        "",
        "[Sensors]",
        f"LiDAR       : {config.sensors.lidar}",
        f"Camera      : {config.sensors.camera}",
        f"IMU         : {config.sensors.imu}",
        f"GPS         : {config.sensors.gps}",
        f"Radar       : {config.sensors.radar}",
        "",
        "[Detection]",
        (
            "Confidence : "
            f"{config.detection.confidence_threshold:.2f}"
        ),
        (
            "Maximum    : "
            f"{config.detection.maximum_faults}"
        ),
        (
            "GPU        : "
            f"{config.detection.enable_gpu}"
        ),
        "",
        "[Output]",
        f"Directory  : {config.output.directory}",
        f"JSON       : {config.output.save_json}",
        f"CSV        : {config.output.save_csv}",
        f"Images     : {config.output.save_images}",
    ]

    return "\n".join(lines)


def print_configuration(
    config: FLDRConfig,
) -> None:
    """Print the current configuration."""

    print(configuration_summary(config))


def export_configuration(
    config: FLDRConfig,
    path: Path,
) -> None:
    """Export the configuration according to the file extension."""

    suffix = path.suffix.lower()

    if suffix == ".json":
        save_json(config, path)
        return

    msg = (
        "Unsupported configuration format. "
        "Only JSON export is currently supported."
    )
    raise ConfigurationError(msg)


def is_gpu_enabled(
    config: FLDRConfig,
) -> bool:
    """Return whether GPU acceleration is enabled."""

    return config.detection.enable_gpu


def is_sensor_enabled(
    config: FLDRConfig,
    sensor: str,
) -> bool:
    """Return whether a sensor is enabled."""

    sensors = {
        "lidar": config.sensors.lidar,
        "camera": config.sensors.camera,
        "imu": config.sensors.imu,
        "gps": config.sensors.gps,
        "radar": config.sensors.radar,
        "wheel_encoder": config.sensors.wheel_encoder,
    }

    return sensors.get(sensor.lower(), False)


def enable_gpu(
    config: FLDRConfig,
) -> None:
    """Enable GPU acceleration."""

    config.detection.enable_gpu = True


def disable_gpu(
    config: FLDRConfig,
) -> None:
    """Disable GPU acceleration."""

    config.detection.enable_gpu = False
    
