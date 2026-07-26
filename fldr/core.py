"""Core interfaces for the FLDR package."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class DetectionResult:
    """Represents a single detected pipeline fault."""

    fault_type: str
    confidence: float
    position_m: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def is_valid(self) -> bool:
        """Return True if the detection result is valid."""
        return (
            0.0 <= self.confidence <= 1.0
            and self.position_m >= 0.0
            and bool(self.fault_type)
        )


@dataclass(slots=True)
class InspectionReport:
    """Represents the result of an inspection."""

    timestamp: datetime = field(default_factory=datetime.utcnow)
    detector: str = "FLDR"
    pipeline_type: str = "unknown"
    results: list[DetectionResult] = field(default_factory=list)

    @property
    def fault_count(self) -> int:
        """Return the total number of detected faults."""
        return len(self.results)

    def add(self, result: DetectionResult) -> None:
        """Add a detection result."""
        self.results.append(result)

    def clear(self) -> None:
        """Remove all detection results."""
        self.results.clear()


class FLDRCore:
    """Core FLDR interface."""

    def __init__(self) -> None:
        """Initialize the FLDR core."""
        self._report = InspectionReport()

    @property
    def report(self) -> InspectionReport:
        """Return the current inspection report."""
        return self._report

    def detect(
        self,
        fault_type: str,
        confidence: float,
        position_m: float,
        **metadata: Any,
    ) -> DetectionResult:
        """Create and store a detection result."""
        result = DetectionResult(
            fault_type=fault_type,
            confidence=confidence,
            position_m=position_m,
            metadata=metadata,
        )

        if not result.is_valid():
            raise ValueError("Invalid detection result.")

        self._report.add(result)
        return result

    def reset(self) -> None:
        """Reset the inspection report."""
        self._report = InspectionReport()
