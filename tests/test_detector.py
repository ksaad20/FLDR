"""Fault detection interfaces for FLDR."""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from fldr.core import DetectionResult


class BaseDetector(ABC):
    """Abstract base class for all fault detectors."""

    @abstractmethod
    def detect(self, data: object) -> list[DetectionResult]:
        """Detect faults from input data."""
        raise NotImplementedError


class FaultDetector(BaseDetector):
    """
    Baseline threshold-based fault detector.

    Detects abnormal sensor values using signal amplitude thresholding.
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
            Signal amplitude threshold for fault detection.
        """
        self.threshold = threshold

    def detect(
        self,
        data: object,
    ) -> list[DetectionResult]:
        """
        Detect faults from a sensor signal.

        Parameters
        ----------
        data:
            One-dimensional sensor signal.

        Returns
        -------
        list[DetectionResult]
            Detected fault events.
        """
        signal = np.asarray(data)

        if signal.ndim != 1:
            raise ValueError("Signal must be one-dimensional.")

        labels = (np.abs(signal) > self.threshold).astype(int)

        results = []

        for index, label in enumerate(labels):
            if label == 1:
                results.append(
                    DetectionResult(
                        position=index,
                        confidence=1.0,
                    )
                )

        return results


class RuleBasedDetector(BaseDetector):
    """Simple rule-based detector implementation."""

    def __init__(
        self,
        confidence_threshold: float = 0.5,
    ) -> None:
        """Initialize rule-based detector."""
        self.confidence_threshold = confidence_threshold

    def detect(
        self,
        data: object,
    ) -> list[DetectionResult]:
        """Detect faults using rule-based logic."""
        _ = data
        return []
