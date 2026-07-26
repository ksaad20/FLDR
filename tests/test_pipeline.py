"""Tests for the FLDR pipeline module."""

from __future__ import annotations

import pytest

from fldr.pipeline import Pipeline


class TestPipeline:
    """Tests for the Pipeline class."""

    def test_default_values(self) -> None:
        """Test default pipeline values."""
        pipeline = Pipeline()

        assert pipeline.pipeline_type == "oil"
        assert pipeline.material == "steel"
        assert pipeline.diameter_m == 0.5
        assert pipeline.length_m == 1000.0

    def test_validate_valid_pipeline(self) -> None:
        """Validation should succeed for a valid pipeline."""
        pipeline = Pipeline()

        pipeline.validate()

    def test_validate_invalid_diameter(self) -> None:
        """Validation should fail for a non-positive diameter."""
        pipeline = Pipeline(diameter_m=0.0)

        with pytest.raises(ValueError):
            pipeline.validate()

    def test_validate_invalid_length(self) -> None:
        """Validation should fail for a non-positive length."""
        pipeline = Pipeline(length_m=0.0)

        with pytest.raises(ValueError):
            pipeline.validate()

    def test_radius(self) -> None:
        """Test radius calculation."""
        pipeline = Pipeline(diameter_m=1.0)

        assert pipeline.radius_m == 0.5

    def test_circumference(self) -> None:
        """Test circumference calculation."""
        pipeline = Pipeline(diameter_m=1.0)

        assert pipeline.circumference_m == pytest.approx(3.141592653589793)

    def test_cross_sectional_area(self) -> None:
        """Test cross-sectional area calculation."""
        pipeline = Pipeline(diameter_m=2.0)

        assert pipeline.cross_sectional_area_m2 == pytest.approx(3.141592653589793)

    def test_to_dict(self) -> None:
        """Test dictionary conversion."""
        pipeline = Pipeline()

        data = pipeline.to_dict()

        assert data["pipeline_type"] == "oil"
        assert data["material"] == "steel"
        assert data["diameter_m"] == 0.5
        assert data["length_m"] == 1000.0

    def test_from_dict(self) -> None:
        """Test construction from a dictionary."""
        data = {
            "pipeline_type": "gas",
            "material": "PVC",
            "diameter_m": 0.75,
            "length_m": 500.0,
        }

        pipeline = Pipeline.from_dict(data)

        assert pipeline.pipeline_type == "gas"
        assert pipeline.material == "PVC"
        assert pipeline.diameter_m == 0.75
        assert pipeline.length_m == 500.0

    def test_copy(self) -> None:
        """Test copying a pipeline."""
        pipeline = Pipeline(
            pipeline_type="gas",
            material="PVC",
            diameter_m=0.75,
            length_m=500.0,
        )

        copied = pipeline.copy()

        assert copied == pipeline
        assert copied is not pipeline
