"""
Simulation utilities for generating synthetic pipe fault signals.

This module provides a configurable simulator for generating sensor-like
signals containing fault events. It is intended for testing and benchmarking
fault line detection algorithms.
"""

from __future__ import annotations

import numpy as np

from fldr.config import SimulationConfig


class FaultSimulator:
    """Generate synthetic signals with simulated pipe faults."""

    def __init__(self, config: SimulationConfig) -> None:
        """
        Initialize the fault simulator.

        Parameters
        ----------
        config:
            Simulation configuration containing signal parameters,
            fault characteristics, and random seed.
        """
        self.config = config
        self.rng = np.random.default_rng(config.seed)

    def generate(self) -> dict[str, np.ndarray]:
        """
        Generate a synthetic fault signal.

        Returns
        -------
        dict[str, np.ndarray]
            Dictionary containing:
            - position: sample positions
            - signal: generated sensor signal
            - labels: binary fault labels
        """
        n = self.config.signal_length

        signal = self.rng.normal(
            loc=0.0,
            scale=self.config.noise_level,
            size=n,
        )

        labels = np.zeros(
            n,
            dtype=int,
        )

        for _ in range(self.config.num_faults):
            index = self.rng.integers(
                low=0,
                high=n,
            )

            width = self.rng.integers(
                low=5,
                high=20,
            )

            end = min(
                index + width,
                n,
            )

            fault_signal = (
                self.config.fault_amplitude * self.rng.random()
            )

            signal[index:end] += fault_signal

            labels[index:end] = 1

        return {
            "position": np.arange(n),
            "signal": signal,
            "labels": labels,
        }
