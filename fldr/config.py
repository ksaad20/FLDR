"""Configuration management for FLDR."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
import os


class ConfigurationError(ValueError):
    """Raised when the configuration is invalid."""


@dataclass(slots=True)
class PipelineConfig:
    """Pipeline-specific settings."""

    pipeline_type: str = "oil"
    diameter_m: float = 0.5
    inspection_length_m: float = 1000.0
    material: str = "steel"


@dataclass(slots=True)
class SensorConfig:
    """Sensor settings."""

    camera: bool = True
    lidar: bool = True
    imu: bool = True
    gps: bool = False
    ultrasonic: bool = False
    sampling_frequency_hz: float = 20.0


@dataclass(slots=True)
class DetectionConfig:
    """Detection settings."""

    confidence_threshold: float = 0.5
    enable_gpu: bool = False
    detect_corrosion: bool = True
    detect_cracks: bool = True
    detect_leaks: bool = True


@dataclass(slots=True)
class OutputConfig:
    """Output settings."""

    directory: Path = Path("output")
    save_json: bool = True
    save_csv: bool = True
    save_images: bool = True


@dataclass(slots=True)
class FLDRConfig:
    """Top-level configuration."""

    pipeline: PipelineConfig = field(default_factory=PipelineConfig)
    sensors: SensorConfig = field(default_factory=SensorConfig)
    detection: DetectionConfig = field(default_factory=DetectionConfig)
    output: OutputConfig = field(default_factory=OutputConfig)

    def validate(self) -> None:
        """Validate configuration."""

        if not 0.0 <= self.detection.confidence_threshold <= 1.0:
            raise ConfigurationError(
                "confidence_threshold must be between 0.0 and 1.0."
            )

        if self.pipeline.diameter_m <= 0:
            raise ConfigurationError("pipeline diameter must be positive.")

        if self.pipeline.inspection_length_m <= 0:
            raise ConfigurationError("inspection length must be positive.")

        if self.sensors.sampling_frequency_hz <= 0:
            raise ConfigurationError(
                "sampling_frequency_hz must be positive."
            )


def create_default_config() -> FLDRConfig:
    """Return a validated default configuration."""

    config = FLDRConfig()
    config.validate()
    return config


def load_environment(config: FLDRConfig) -> FLDRConfig:
    """Apply environment variable overrides."""

    if value := os.getenv("FLDR_OUTPUT_DIRECTORY"):
        config.output.directory = Path(value)

    if value := os.getenv("FLDR_CONFIDENCE_THRESHOLD"):
        config.detection.confidence_threshold = float(value)

    if value := os.getenv("FLDR_ENABLE_GPU"):
        config.detection.enable_gpu = value.lower() in {
            "1",
            "true",
            "yes",
            "on",
        }

    config.validate()
    return config


def configuration_to_dict(config: FLDRConfig) -> dict[str, object]:
    """Return a serializable representation."""

    return asdict(config)


__all__ = [
    "ConfigurationError",
    "PipelineConfig",
    "SensorConfig",
    "DetectionConfig",
    "OutputConfig",
    "FLDRConfig",
    "create_default_config",
    "load_environment",
    "configuration_to_dict",
]
