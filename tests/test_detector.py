"""Tests for FLDR fault detection module."""

import numpy as np

from fldr.detector import FaultDetector


def test_detector_initialization():
    """Test detector can be initialized."""
    detector = FaultDetector()

    assert detector is not None


def test_detector_detect_method_exists():
    """Test detector exposes detection interface."""
    detector = FaultDetector()

    assert hasattr(detector, "detect")


def test_detector_returns_result():
    """Test detector returns output for a valid signal."""
    detector = FaultDetector()

    signal = np.zeros(100)

    result = detector.detect(signal)

    assert result is not None


def test_detector_handles_fault_signal():
    """Test detector processes a signal containing a fault."""
    detector = FaultDetector()

    signal = np.zeros(100)
    signal[50:60] = 10.0

    result = detector.detect(signal)

    assert result is not None


def test_detector_handles_numpy_input():
    """Test detector accepts numpy arrays."""
    detector = FaultDetector()

    signal = np.random.default_rng(42).normal(
        0,
        1,
        200,
    )

    result = detector.detect(signal)

    assert result is not None


def test_detector_output_shape():
    """Test detector output has expected length if array based."""
    detector = FaultDetector()

    signal = np.zeros(100)

    result = detector.detect(signal)

    if isinstance(result, np.ndarray):
        assert len(result) == len(signal)
