"""Fault detection interfaces for FLDR."""

from __future__ import annotations

from abc import ABC, abstractmethod

from fldr.core import DetectionResult


class BaseDetector(ABC):
    """Abstract base class for all fault detectors."""

    @abstractmethod
    def detect(self, data: object) -> list[DetectionResult]:
        """Detect faults from input data."""
        raise NotImplementedError


class RuleBasedDetector(BaseDetector):
    """Simple threshold-based detector."""

    def __init__(self, confidence_threshold: float = 0.5) -> None:
        """Initialize the detector."""
        self.confidence_threshold = confidence_threshold

    def detect(self, data: object) -> list[DetectionResult]:
        """Detect faults.

        This placeholder implementation returns no detections.
        Future releases will implement computer vision and sensor
        fusion algorithms here.
        """
        _ = data
        return []
