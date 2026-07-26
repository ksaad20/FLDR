"""Pipeline models for FLDR."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Pipeline:
    """Represents a pipeline under inspection."""

    pipeline_type: str = "oil"
    material: str = "steel"
    diameter_m: float = 0.5
    length_m: float = 1000.0

    def validate(self) -> None:
        """Validate pipeline properties."""
        if self.diameter_m <= 0.0:
            raise ValueError("Pipeline diameter must be positive.")

        if self.length_m <= 0.0:
            raise ValueError("Pipeline length must be positive.")

        if not self.pipeline_type:
            raise ValueError("Pipeline type cannot be empty.")

        if not self.material:
            raise ValueError("Pipeline material cannot be empty.")

    @property
    def radius_m(self) -> float:
        """Return the pipeline radius."""
        return self.diameter_m / 2.0

    @property
    def circumference_m(self) -> float:
        """Return the pipeline circumference."""
        return self.diameter_m * 3.141592653589793

    @property
    def cross_sectional_area_m2(self) -> float:
        """Return the pipeline cross-sectional area."""
        radius = self.radius_m
        return 3.141592653589793 * radius * radius

    def to_dict(self) -> dict[str, float | str]:
        """Return the pipeline as a dictionary."""
        return {
            "pipeline_type": self.pipeline_type,
            "material": self.material,
            "diameter_m": self.diameter_m,
            "length_m": self.length_m,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Pipeline":
        """Create a pipeline from a dictionary."""
        return cls(
            pipeline_type=str(data.get("pipeline_type", "oil")),
            material=str(data.get("material", "steel")),
            diameter_m=float(data.get("diameter_m", 0.5)),
            length_m=float(data.get("length_m", 1000.0)),
        )

    def copy(self) -> "Pipeline":
        """Return a copy of the pipeline."""
        return Pipeline(
            pipeline_type=self.pipeline_type,
            material=self.material,
            diameter_m=self.diameter_m,
            length_m=self.length_m,
        )
