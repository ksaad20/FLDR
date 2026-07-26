"""
Simulation utilities for generating synthetic pipe fault signals.

This module provides synthetic signal generation for testing fault detection
algorithms in the FLDR framework.
"""

from __future__ import annotations

import numpy as np

from fldr.config import SimulationConfig


class FaultSimulator:
    """Synthetic pipe fault signal generator."""

    def __init__(self, config: SimulationConfig) -> None:
        """
        Initialize the simulator.

        Parameters
        ----------
        config:
            Simulation configuration parameters.
        """
        self.config = config
        self.rng = np.random.default_rng(config.seed)

    def generate(self) -> dict[str, np.ndarray]:
        """
        Generate a synthetic signal containing fault regions.

        Returns
        -------
        dict[str, np.ndarray]
            Generated position, signal, and fault labels.
        """
        signal_length = self.config.signal_length

        signal = self.rng.normal(
            loc=0.0,
            scale=self.config.noise_level,
            size=signal_length,
        )

        labels = np.zeros(
            signal_length,
            dtype=int,
        )

        for _ in range(self.config.num_faults):
            fault_start = self.rng.integers(
                low=0,
                high=signal_length,
            )

            fault_width = self.rng.integers(
                low=5,
                high=20,
            )

            fault_end = min(
                fault_start + fault_width,
                signal_length,
            )

            fault_strength = self.config.fault_amplitude * self.rng.random()

            signal[fault_start:fault_end] += fault_strength

            labels[fault_start:fault_end] = 1

        return {
            "position": np.arange(signal_length),
            "signal": signal,
            "labels": labels,
        }
