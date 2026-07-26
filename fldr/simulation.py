"""
FLDR simulation module.

Generates synthetic pipe inspection sensor data
for testing fault detection algorithms.
"""

from dataclasses import dataclass
from typing import Dict

import numpy as np


@dataclass
class SimulationConfig:
    """Configuration for pipe fault simulation."""

    length: int = 1000
    noise_level: float = 0.05
    fault_probability: float = 0.02
    fault_amplitude: float = 1.0
    seed: int = 42


class PipeSimulator:
    """
    Simulates robotic pipe inspection sensor streams.

    Generates:
    - baseline sensor readings
    - pipe anomalies
    - fault labels
    """

    def __init__(
        self,
        config: SimulationConfig | None = None,
    ):
        self.config = config or SimulationConfig()
        self.rng = np.random.default_rng(self.config.seed)

    def generate(
        self,
    ) -> Dict[str, np.ndarray]:
        """
        Generate synthetic inspection data.

        Returns
        -------
        dict:
            sensor data and fault labels.
        """

        n = self.config.length

        signal = self.rng.normal(
            loc=0.0,
            scale=self.config.noise_level,
            size=n,
        )

        labels = np.zeros(n, dtype=int)

        faults = self.rng.random(n) < (self.config.fault_probability)

        for index in np.where(faults)[0]:
            width = self.rng.integers(
                low=5,
                high=20,
            )

            end = min(
                index + width,
                n,
            )

            signal[index:end] += (
                self.config.fault_amplitude * self.rng.random()
            )

            labels[index:end] = 1

        return {
            "position": np.arange(n),
            "sensor_signal": signal,
            "fault_labels": labels,
        }


def simulate_inspection(
    length: int = 1000,
) -> Dict[str, np.ndarray]:
    """
    Convenience function for quick simulations.
    """

    simulator = PipeSimulator(SimulationConfig(length=length))

    return simulator.generate()


if __name__ == "__main__":
    data = simulate_inspection()

    print(
        "Generated samples:",
        len(data["sensor_signal"]),
    )

    print(
        "Detected fault points:",
        data["fault_labels"].sum(),
    )
