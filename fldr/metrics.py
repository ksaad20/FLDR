"""Evaluation metrics for FLDR fault detection."""

from __future__ import annotations

import numpy as np


def _validate_inputs(
    ground_truth: np.ndarray,
    predictions: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Validate metric inputs."""
    truth = np.asarray(ground_truth)
    predicted = np.asarray(predictions)

    if truth.shape != predicted.shape:
        raise ValueError("Inputs must have identical shapes.")

    return truth, predicted


def accuracy(
    ground_truth: np.ndarray,
    predictions: np.ndarray,
) -> float:
    """
    Calculate detection accuracy.

    Parameters
    ----------
    ground_truth:
        True fault labels.
    predictions:
        Predicted fault labels.

    Returns
    -------
    float
        Accuracy score.
    """
    truth, predicted = _validate_inputs(
        ground_truth,
        predictions,
    )

    return float(np.mean(truth == predicted))


def precision(
    ground_truth: np.ndarray,
    predictions: np.ndarray,
) -> float:
    """
    Calculate precision.

    Precision measures how many detected faults
    are actual faults.
    """
    truth, predicted = _validate_inputs(
        ground_truth,
        predictions,
    )

    true_positive = np.sum((truth == 1) & (predicted == 1))
    false_positive = np.sum((truth == 0) & (predicted == 1))

    denominator = true_positive + false_positive

    if denominator == 0:
        return 0.0

    return float(true_positive / denominator)


def recall(
    ground_truth: np.ndarray,
    predictions: np.ndarray,
) -> float:
    """
    Calculate recall.

    Recall measures how many real faults
    were successfully detected.
    """
    truth, predicted = _validate_inputs(
        ground_truth,
        predictions,
    )

    true_positive = np.sum((truth == 1) & (predicted == 1))
    false_negative = np.sum((truth == 1) & (predicted == 0))

    denominator = true_positive + false_negative

    if denominator == 0:
        return 0.0

    return float(true_positive / denominator)


def f1_score(
    ground_truth: np.ndarray,
    predictions: np.ndarray,
) -> float:
    """
    Calculate F1 score.
    """
    precision_value = precision(
        ground_truth,
        predictions,
    )

    recall_value = recall(
        ground_truth,
        predictions,
    )

    denominator = precision_value + recall_value

    if denominator == 0:
        return 0.0

    return float(
        2
        * (precision_value * recall_value)
        / denominator,
    )


def false_alarm_rate(
    ground_truth: np.ndarray,
    predictions: np.ndarray,
) -> float:
    """
    Calculate false alarm rate.

    Measures false detections among normal samples.
    """
    truth, predicted = _validate_inputs(
        ground_truth,
        predictions,
    )

    false_positive = np.sum((truth == 0) & (predicted == 1))
    true_negative = np.sum((truth == 0) & (predicted == 0))

    denominator = false_positive + true_negative

    if denominator == 0:
        return 0.0

    return float(false_positive / denominator)
