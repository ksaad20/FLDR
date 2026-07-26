"""Tests for the FLDR configuration module."""

from __future__ import annotations

from pathlib import Path

import pytest

from fldr.config import (
    ConfigurationError,
    FLDRConfig,
    create_default_config,
    load_environment,
)


class TestCreateDefaultConfig:
    """Tests for create_default_config()."""

    def test_returns_config(self) -> None:
        """The default factory should return a valid configuration."""
        config = create_default_config()

        assert isinstance(config, FLDRConfig)

    def test_default_config_is_valid(self) -> None:
        """The default configuration should validate successfully."""
        config = create_default_config()

        config.validate()


class TestValidation:
    """Tests for configuration validation."""

    def test_invalid_confidence_threshold_low(self) -> None:
        """Confidence threshold below zero should fail."""
        config = FLDRConfig()
        config.detection.confidence_threshold = -0.1

        with pytest.raises(ConfigurationError):
            config.validate()

    def test_invalid_confidence_threshold_high(self) -> None:
        """Confidence threshold above one should fail."""
        config = FLDRConfig()
        config.detection.confidence_threshold = 1.1

        with pytest.raises(ConfigurationError):
            config.validate()

    def test_invalid_pipeline_diameter(self) -> None:
        """Pipeline diameter must be positive."""
        config = FLDRConfig()
        config.pipeline.diameter_m = 0.0

        with pytest.raises(ConfigurationError):
            config.validate()

    def test_invalid_inspection_length(self) -> None:
        """Inspection length must be positive."""
        config = FLDRConfig()
        config.pipeline.inspection_length_m = -1.0

        with pytest.raises(ConfigurationError):
            config.validate()

    def test_invalid_sampling_frequency(self) -> None:
        """Sampling frequency must be positive."""
        config = FLDRConfig()
        config.sensors.sampling_frequency_hz = 0.0

        with pytest.raises(ConfigurationError):
            config.validate()


class TestEnvironmentLoading:
    """Tests for environment variable loading."""

    def test_output_directory(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Output directory should be read from the environment."""
        monkeypatch.setenv("FLDR_OUTPUT_DIRECTORY", "results")

        config = load_environment(FLDRConfig())

        assert config.output.directory == Path("results")

    def test_confidence_threshold(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Confidence threshold should be read from the environment."""
        monkeypatch.setenv("FLDR_CONFIDENCE_THRESHOLD", "0.75")

        config = load_environment(FLDRConfig())

        assert config.detection.confidence_threshold == 0.75

    @pytest.mark.parametrize("value", ["1", "true", "yes", "on"])
    def test_gpu_enabled(
        self,
        monkeypatch: pytest.MonkeyPatch,
        value: str,
    ) -> None:
        """Truthy values should enable GPU support."""
        monkeypatch.setenv("FLDR_ENABLE_GPU", value)

        config = load_environment(FLDRConfig())

        assert config.detection.enable_gpu is True

    @pytest.mark.parametrize("value", ["0", "false", "no", "off"])
    def test_gpu_disabled(
        self,
        monkeypatch: pytest.MonkeyPatch,
        value: str,
    ) -> None:
        """Falsy values should disable GPU support."""
        monkeypatch.setenv("FLDR_ENABLE_GPU", value)

        config = load_environment(FLDRConfig())

        assert config.detection.enable_gpu is False
