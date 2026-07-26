"""Reporting utilities for FLDR."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class InspectionReport:
    """Summary of a pipe inspection."""

    fault_detected: bool
    confidence: float
    fault_location: float | None = None
    metrics: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return the report as a dictionary."""
        return {
            "fault_detected": self.fault_detected,
            "confidence": self.confidence,
            "fault_location": self.fault_location,
            "metrics": self.metrics,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InspectionReport":
        """Create an inspection report from a dictionary."""
        return cls(
            fault_detected=data.get("fault_detected", False),
            confidence=float(data.get("confidence", 0.0)),
            fault_location=data.get("fault_location"),
            metrics=dict(data.get("metrics", {})),
            metadata=dict(data.get("metadata", {})),
        )

    def __str__(self) -> str:
        """Return a human-readable summary."""
        location = (
            f"{self.fault_location:.2f} m"
            if self.fault_location is not None
            else "Unknown"
        )

        return (
            "InspectionReport("
            f"fault_detected={self.fault_detected}, "
            f"confidence={self.confidence:.3f}, "
            f"fault_location={location}"
            ")"
      )
