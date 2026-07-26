"""Tests for fault simulation module."""

import numpy as np

from fldr.config import SimulationConfig
from fldr.simulation import FaultSimulator


def test_simulation_output_structure():
    config = SimulationConfig(
        signal_length=100,
        num_faults=2,
        seed=42,
    )

    result = FaultSimulator(config).generate()

    assert set(result.keys()) == {
        "position",
        "signal",
        "labels",
    }


def test_simulation_output_length():
    config = SimulationConfig(
        signal_length=100,
        seed=42,
    )

    result = FaultSimulator(config).generate()

    assert len(result["position"]) == 100
    assert len(result["signal"]) == 100
    assert len(result["labels"]) == 100


def test_fault_labels_exist():
    config = SimulationConfig(
        signal_length=200,
        num_faults=3,
        seed=42,
    )

    result = FaultSimulator(config).generate()

    assert np.sum(result["labels"]) > 0


def test_labels_are_binary():
    config = SimulationConfig(seed=42)

    result = FaultSimulator(config).generate()

    assert np.all(np.isin(result["labels"], [0, 1]))


def test_reproducible_results():
    config = SimulationConfig(
        signal_length=100,
        seed=123,
    )

    first = FaultSimulator(config).generate()
    second = FaultSimulator(config).generate()

    np.testing.assert_array_equal(
        first["signal"],
        second["signal"],
    )

    np.testing.assert_array_equal(
        first["labels"],
        second["labels"],
    )
