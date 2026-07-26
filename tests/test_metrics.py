"""Tests for FLDR evaluation metrics."""

import numpy as np
import pytest

from metrics.metrics import (
    accuracy,
    f1_score,
    false_alarm_rate,
    precision,
    recall,
)


def test_accuracy_perfect_prediction():
    """Test accuracy returns one for perfect predictions."""
    truth = np.array([0, 1, 0, 1])
    prediction = np.array([0, 1, 0, 1])

    result = accuracy(
        truth,
        prediction,
    )

    assert result == 1.0


def test_precision_calculation():
    """Test precision metric."""
    truth = np.array([0, 1, 1, 0])
    prediction = np.array([0, 1, 0, 0])

    result = precision(
        truth,
        prediction,
    )

    assert result == 1.0


def test_recall_calculation():
    """Test recall metric."""
    truth = np.array([0, 1, 1, 0])
    prediction = np.array([0, 1, 0, 0])

    result = recall(
        truth,
        prediction,
    )

    assert result == 0.5


def test_f1_score_calculation():
    """Test F1 score metric."""
    truth = np.array([0, 1, 1, 0])
    prediction = np.array([0, 1, 0, 0])

    result = f1_score(
        truth,
        prediction,
    )

    assert result == pytest.approx(0.666666, rel=1e-5)


def test_false_alarm_rate_calculation():
    """Test false alarm rate metric."""
    truth = np.array([0, 0, 1, 1])
    prediction = np.array([1, 0, 1, 0])

    result = false_alarm_rate(
        truth,
        prediction,
    )

    assert result == 0.5


def test_metrics_accept_numpy_arrays():
    """Test metrics support numpy inputs."""
    truth = np.zeros(10)
    prediction = np.zeros(10)

    assert accuracy(truth, prediction) == 1.0


def test_metrics_reject_mismatched_shapes():
    """Test metrics reject different input sizes."""
    truth = np.array([0, 1, 0])
    prediction = np.array([0, 1])

    with pytest.raises(ValueError):
        accuracy(
            truth,
            prediction,
        )


def test_metrics_handle_zero_division():
    """Test metrics return zero when no positive cases exist."""
    truth = np.zeros(10)
    prediction = np.zeros(10)

    assert precision(truth, prediction) == 0.0
    assert recall(truth, prediction) == 0.0
    assert f1_score(truth, prediction) == 0.0
