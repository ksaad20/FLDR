"""
Synthetic signal simulation module for Fault Line Detection Robotics (FLDR).

This module generates realistic pipe inspection signals with configurable
noise, fault locations, and fault amplitudes. It is designed for testing
fault detection algorithms before deployment on real robotic sensor data.
"""

from __future__ import annotations

import numpy as np

from fldr.config import SimulationConfig


class FaultSimulator:
    """
    Simulator for generating synthetic pipe fault sensor data.

    Parameters
    ----------
    config:
        Simulation configuration object containing signal generation
        parameters.
    """

    def __init__(self, config: SimulationConfig) -> None:
        self.config = config
        self.rng = np.random.default_rng(config.seed)

    def generate_signal(self) -> dict[str, np.ndarray]:
        """
        Generate a synthetic pipe inspection signal.

        Returns
        -------
        dict[str, np.ndarray]
            Generated signal data containing:
            - position: sensor sample positions
            - signal: simulated sensor response
            - labels: binary fault annotations
        """
        signal_length = self.config.signal_length

        signal = self.rng.normal(
            loc=0.0,
            scale=self.config.noise_level,
            size=signal_length,
        )

        labels = np.zeros(
            signal_length,
            dtype=np.int32,
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

            fault_strength = (
                self.config.fault_amplitude * self.rng.random()
            )

            signal[fault_start:fault_end] += fault_strength

            labels[fault_start:fault_end] = 1

        return {
            "position": np.arange(signal_length),
            "signal": signal,
            "labels": labels,
        }

    def add_noise(
        self,
        signal: np.ndarray,
    ) -> np.ndarray:
        """
        Add measurement noise to an existing signal.

        Parameters
        ----------
        signal:
            Input sensor signal.

        Returns
        -------
        np.ndarray
            Noisy sensor signal.
        """
        noise = self.rng.normal(
            loc=0.0,
            scale=self.config.noise_level,
            size=signal.shape,
        )

        return signal + noise
