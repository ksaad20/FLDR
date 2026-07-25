"""
FLDR Configuration Module
=========================

Lightweight configuration system for pipeline inspection.

Author
------
FLDR Development Team
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
import os


class ConfigurationError(ValueError):
    """Raised when the configuration is invalid."""


@dataclass(slots=True)
class GeneralConfig:
    """General application settings."""

    application_name: str = "FLDR"
    version: str = "0.1.0"
    workspace: Path = Path.cwd()
    temporary_directory: Path = Path.cwd() / "tmp"


@dataclass(slots=True)
class PipelineConfig:
    """Pipeline information."""

    pipeline_type: str = "oil"
    diameter_m: float = 0.5
    material: str = "steel"
    inspection_length_m: float = 1000.0


@dataclass(slots=True)
class SensorConfig:
    """Sensor configuration."""

    camera: bool = True
    lidar: bool = True
    imu: bool = True
    gps: bool = False
    ultrasonic: bool = False
    sampling_frequency_hz: float = 20.0


@dataclass(slots=True)
class DetectionConfig:
    """Inspection parameters."""

    confidence_threshold: float = 0.5
    minimum_defect_size_mm: float = 2.0
    detect_corrosion: bool = True
    detect_cracks: bool = True
    detect_leaks: bool = True
    enable_gpu: bool = False


@dataclass(slots=True)
class OutputConfig:
    """Output settings."""

    directory: Path = Path("output")
    save_json: bool = True
    save_csv: bool = True
    save_images: bool = True


@dataclass(slots=True)
class LoggingConfig:
    """Logging configuration."""

    enabled: bool = True
    level: str = "INFO"
    file: str = "fldr.log"


@dataclass(slots=True)
class FLDRConfig:
    """Root configuration."""

    general: GeneralConfig = field(default_factory=GeneralConfig)
    pipeline: PipelineConfig = field(default_factory=PipelineConfig)
    sensors: SensorConfig = field(default_factory=SensorConfig)
    detection: DetectionConfig = field(default_factory=DetectionConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)

    def validate(self) -> None:
        """Validate configuration values."""

        if not 0.0 <= self.detection.confidence_threshold <= 1.0:
            raise ConfigurationError(
                "confidence_threshold must be between 0.0 and 1.0."
            )

        if self.pipeline.diameter_m <= 0:
            raise ConfigurationError("pipeline diameter must be positive.")

        if self.pipeline.inspection_length_m <= 0:
            raise ConfigurationError(
                "inspection length must be positive."
            )

        if self.sensors.sampling_frequency_hz <= 0:
            raise ConfigurationError(
                "sampling_frequency_hz must be positive."
            )


def create_default_config() -> FLDRConfig:
    """Create and validate the default configuration."""

    config = FLDRConfig()
    config.validate()
    return config


def apply_environment(config: FLDRConfig) -> FLDRConfig:
    """Apply environment variable overrides."""

    level = os.getenv("FLDR_LOG_LEVEL")
    if level:
        config.logging.level = level.upper()

    gpu = os.getenv("FLDR_ENABLE_GPU")
    if gpu:
        config.detection.enable_gpu = gpu.lower() in {
            "1",
            "true",
            "yes",
            "on",
        }

    workspace = os.getenv("FLDR_WORKSPACE")
    if workspace:
        config.general.workspace = Path(workspace)

    output = os.getenv("FLDR_OUTPUT_DIRECTORY")
    if output:
        config.output.directory = Path(output)

    config.validate()
    return config


def configuration_to_dict(config: FLDRConfig) -> dict[str, object]:
    """Convert the configuration to a serializable dictionary."""

    return asdict(config)


__all__ = [
    "ConfigurationError",
    "GeneralConfig",
    "PipelineConfig",
    "SensorConfig",
    "DetectionConfig",
    "OutputConfig",
    "LoggingConfig",
    "FLDRConfig",
    "create_default_config",
    "apply_environment",
    "configuration_to_dict",
]
