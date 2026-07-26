"""Reporting utilities for FLDR."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class InspectionReport:
    """Container for the results of a pipe inspection."""

    fault_detected: bool
    confidence: float
    fault_location: float | None = None
    metrics: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert the report to a dictionary."""
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
            fault_detected=bool(data.get("fault_detected", False)),
            confidence=float(data.get("confidence", 0.0)),
            fault_location=data.get("fault_location"),
            metrics=dict(data.get("metrics", {})),
            metadata=dict(data.get("metadata", {})),
        )

    @property
    def has_fault(self) -> bool:
        """Return whether a fault was detected."""
        return self.fault_detected

    def summary(self) -> str:
        """Return a concise summary of the inspection."""
        if self.fault_detected:
            location = (
                f"{self.fault_location:.2f} m"
                if self.fault_location is not None
                else "Unknown"
            )
            return (
                f"Fault detected "
                f"(confidence={self.confidence:.3f}, "
                f"location={location})."
            )

        return f"No fault detected (confidence={self.confidence:.3f})."

    def __str__(self) -> str:
        """Return a human-readable representation."""
        return self.summary()

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return (
            "InspectionReport("
            f"fault_detected={self.fault_detected!r}, "
            f"confidence={self.confidence!r}, "
            f"fault_location={self.fault_location!r}, "
            f"metrics={self.metrics!r}, "
            f"metadata={self.metadata!r}"
            ")"
        )
