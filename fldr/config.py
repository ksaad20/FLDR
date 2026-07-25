"""Configuration management for the FLDR framework."""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
import json
import os
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None

__all__ = [
    "ConfigurationError",
    "GeneralConfig",
    "LoggingConfig",
    "SensorConfig",
    "DetectionConfig",
    "OutputConfig",
    "FLDRConfig",
    "DEFAULT_CONFIG_DIRECTORY",
    "DEFAULT_CONFIG_FILE",
    "create_default_config",
]

DEFAULT_CONFIG_DIRECTORY = Path.home() / ".config" / "fldr"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIRECTORY / "config.toml"


class ConfigurationError(ValueError):
    """Raised when configuration values are invalid."""


@dataclass(slots=True)
class GeneralConfig:
    """General application configuration."""

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
    console: bool = True
    file: bool = True
    directory: Path = Path.cwd() / "logs"
    filename: str = "fldr.log"


@dataclass(slots=True)
class SensorConfig:
    """Sensor configuration."""

    lidar: bool = True
    camera: bool = True
    imu: bool = True
    gps: bool = True
    radar: bool = False
    wheel_encoder: bool = False
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
        """Validate the configuration."""

        if not 0.0 <= self.detection.confidence_threshold <= 1.0:
            msg = "confidence_threshold must be between 0.0 and 1.0."
            raise ConfigurationError(msg)

        if self.detection.maximum_faults < 1:
            msg = "maximum_faults must be greater than zero."
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
    """Return a validated default configuration."""

    config = FLDRConfig()
    config.validate()
return config


def ensure_config_directory() -> Path:
    """Create the default configuration directory."""

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
    """Apply environment variable overrides."""

    log_level = os.getenv("FLDR_LOG_LEVEL")
    if log_level:
        config.logging.level = log_level.upper()

    gpu = os.getenv("FLDR_ENABLE_GPU")
    if gpu:
        config.detection.enable_gpu = gpu.lower() in {
            "1",
            "true",
            "yes",
            "on",
        }

    threshold = os.getenv(
        "FLDR_CONFIDENCE_THRESHOLD",
    )
    if threshold:
        config.detection.confidence_threshold = float(
            threshold,
        )

    workspace = os.getenv("FLDR_WORKSPACE")
    if workspace:
        config.general.workspace = Path(workspace)

    output_directory = os.getenv(
        "FLDR_OUTPUT_DIRECTORY",
    )
    if output_directory:
        config.output.directory = Path(
            output_directory,
        )

    config.validate()

    return config


def configuration_to_dict(
    config: FLDRConfig,
) -> dict[str, object]:
    """Convert a configuration into a serializable dictionary."""

    return {
        "general": {
            "application_name": config.general.application_name,
            "version": config.general.version,
            "workspace": str(
                config.general.workspace,
            ),
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
            "console": config.logging.console,
            "file": config.logging.file,
            "directory": str(
                config.logging.directory,
            ),
            "filename": config.logging.filename,
        },
        "sensors": {
            "lidar": config.sensors.lidar,
            "camera": config.sensors.camera,
            "imu": config.sensors.imu,
            "gps": config.sensors.gps,
            "radar": config.sensors.radar,
            "wheel_encoder": config.sensors.wheel_encoder,
            "sampling_frequency_hz": config.sensors.sampling_frequency_hz,
            "enable_calibration": config.sensors.enable_calibration
            "calibration_directory": config.sensors.calibration_directory,
            "detection": "enabled": config.detection.enabled,
            "confidence_threshold": config.detection.confidence_threshold,
            "minimum_fault_length_m": config.detection.minimum_fault_length_m,
            "maximum_faults": config.detection.maximum_faults,
            "enable_gpu": config.detection.enable_gpu,
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
            "save_point_clouds": config.output.save_point_clouds,
            "overwrite_existing": config.output.overwrite_existing,
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

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            configuration_to_dict(config),
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
        data = json.load(file)

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
    config.logging.level = logging.get(
        "level",
        config.logging.level,
    )
    config.logging.enabled = logging.get(
        "enabled",
        config.logging.enabled,
    )
    config.logging.console = logging.get(
        "console",
        config.logging.console,
    )
    config.logging.file = logging.get(
        "file",
        config.logging.file,
    )

    detection = data.get("detection", {})
    config.detection.confidence_threshold = detection.get(
        "confidence_threshold",
        config.detection.confidence_threshold,
    )
    config.detection.maximum_faults = detection.get(
        "maximum_faults",
        config.detection.maximum_faults,
    )
    config.detection.enable_gpu = detection.get(
        "enable_gpu",
        config.detection.enable_gpu,
    )

    output = data.get("output", {})
    config.output.directory = Path(
        output.get(
            "directory",
            str(config.output.directory),
        ),
    )

    config.validate()

    return config


def load_toml(
    path: Path,
) -> FLDRConfig:
    """Load a configuration from a TOML file."""

    if tomllib is None:
        msg = "tomllib is unavailable."
        raise ConfigurationError(msg)

    with path.open("rb") as file:
        data = tomllib.load(file)

    json_path = path.with_suffix(".json")

    with json_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
        )

    return load_json(json_path)


def discover_configuration() -> Path | None:
    """Return the first configuration file found."""

    candidates = (
        Path.cwd() / "fldr.toml",
        Path.cwd() / "fldr.json",
        DEFAULT_CONFIG_FILE,
        DEFAULT_CONFIG_FILE.with_suffix(".json"),
    )

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return None


def load_configuration() -> FLDRConfig:
    """Load the best available configuration."""

    path = discover_configuration()

    if path is None:
        return load_environment(
            create_default_config(),
        )

    if path.suffix == ".json":
        config = load_json(path)
    elif path.suffix == ".toml":
        config = load_toml(path)
    else:
        config = create_default_config()

    return load_environment(config)

def save_default_configuration() -> Path:
    """Save the default configuration to disk."""

    ensure_config_directory()

    path = DEFAULT_CONFIG_FILE.with_suffix(".json")

    save_json(
        create_default_config(),
        path,
    )

    return path


def reset_configuration() -> FLDRConfig:
    """Return a freshly initialized configuration."""

    return create_default_config()


def configuration_summary(
    config: FLDRConfig,
) -> str:
    """Return a human-readable configuration summary."""

    return "\n".join(
        (
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
            f"Directory   : {config.output.directory}",
            f"JSON        : {config.output.save_json}",
            f"CSV         : {config.output.save_csv}",
            f"Images      : {config.output.save_images}",
            f"PointClouds : {config.output.save_point_clouds}",
        ),
    )


def print_configuration(
    config: FLDRConfig,
) -> None:
    """Print a configuration summary."""

    print(configuration_summary(config))


def export_configuration(
    config: FLDRConfig,
    path: Path,
) -> None:
    """Export a configuration."""

    suffix = path.suffix.lower()

    if suffix == ".json":
        save_json(
            config,
            path,
        )
        return

    msg = "minimum_fault_length_m cannot exceed " "maximum_fault_length_m."
    raise ConfigurationError(msg)


def is_gpu_enabled(
    config: FLDRConfig,
) -> bool:
    """Return whether GPU acceleration is enabled."""

    return config.detection.enable_gpu


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
        "wheel_encoder": (
            config.sensors.wheel_encoder
        ),
    }

    return sensors.get(
        sensor.lower(),
        False,
    )
