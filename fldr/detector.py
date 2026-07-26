"""Fault detection interfaces for FLDR."""

from __future__ import annotations

from abc import ABC, abstractmethod

from fldr.core import DetectionResult

import numpy as np


class FaultDetector:
    """
    Detect faults from sensor signals.

    The current implementation uses amplitude thresholding as a
    baseline detector. Future versions can replace this with ML,
    signal processing, or physics-informed approaches.
    """

    def __init__(
        self,
        threshold: float = 3.0,
    ) -> None:
        """
        Initialize fault detector.

        Parameters
        ----------
        threshold:
            Signal amplitude threshold used for fault detection.
        """
        self.threshold = threshold

    def detect(
        self,
        signal: np.ndarray,
    ) -> np.ndarray:
        """
        Detect fault regions in a sensor signal.

        Parameters
        ----------
        signal:
            One-dimensional sensor signal.

        Returns
        -------
        np.ndarray
            Binary fault labels where:
            0 = normal
            1 = detected fault
        """
        signal = np.asarray(signal)

        if signal.ndim != 1:
            raise ValueError("Signal must be one-dimensional.")

        return (np.abs(signal) > self.threshold).astype(int)


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
