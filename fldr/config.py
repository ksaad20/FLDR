"""Configuration management for FLDR."""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from dataclasses import dataclass

class ConfigurationError(ValueError):
    """Raised when the configuration is invalid."""

@dataclass
class SimulationConfig:
    """Configuration for synthetic fault signal generation."""

    signal_length: int = 1000
    noise_level: float = 0.1
    num_faults: int = 5
    fault_amplitude: float = 1.0
    seed: int = 42


@dataclass(slots=True)
class PipelineConfig:
    """Pipeline-specific settings."""

    pipeline_type: str = "oil"
    diameter_m: float = 0.5
    inspection_length_m: float = 1000.0
    material: str = "steel"


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
    """Detection configuration."""

    confidence_threshold: float = 0.5
    enable_gpu: bool = False
    detect_corrosion: bool = True
    detect_cracks: bool = True
    detect_leaks: bool = True


@dataclass(slots=True)
class OutputConfig:
    """Output configuration."""

    directory: Path = Path("output")
    save_json: bool = True
    save_csv: bool = True
    save_images: bool = True


@dataclass(slots=True)
class FLDRConfig:
    """Top-level FLDR configuration."""

    pipeline: PipelineConfig = field(default_factory=PipelineConfig)
    sensors: SensorConfig = field(default_factory=SensorConfig)
    detection: DetectionConfig = field(default_factory=DetectionConfig)
    output: OutputConfig = field(default_factory=OutputConfig)

    def validate(self) -> None:
        """Validate configuration values."""
        if not 0.0 <= self.detection.confidence_threshold <= 1.0:
            raise ConfigurationError(
                "confidence_threshold must be between 0.0 and 1.0."
            )

        if self.pipeline.diameter_m <= 0.0:
            raise ConfigurationError("Pipeline diameter must be positive.")

        if self.pipeline.inspection_length_m <= 0.0:
            raise ConfigurationError("Inspection length must be positive.")

        if self.sensors.sampling_frequency_hz <= 0.0:
            raise ConfigurationError("sampling_frequency_hz must be positive.")

    def to_dict(self) -> dict[str, object]:
        """Return the configuration as a dictionary."""
        return asdict(self)


def create_default_config() -> FLDRConfig:
    """Create and validate the default configuration."""
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

    if value := os.getenv("FLDR_PIPELINE_TYPE"):
        config.pipeline.pipeline_type = value

    if value := os.getenv("FLDR_PIPELINE_DIAMETER_M"):
        config.pipeline.diameter_m = float(value)

    if value := os.getenv("FLDR_INSPECTION_LENGTH_M"):
        config.pipeline.inspection_length_m = float(value)

    if value := os.getenv("FLDR_PIPELINE_MATERIAL"):
        config.pipeline.material = value

    if value := os.getenv("FLDR_SAMPLING_FREQUENCY_HZ"):
        config.sensors.sampling_frequency_hz = float(value)

    config.validate()
    return config
