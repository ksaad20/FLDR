"""Simulation utilities for FLDR."""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(slots=True)
class SimulatedFault:
    """Represents a simulated pipeline fault."""

    fault_type: str
    position_m: float
    confidence: float


class PipelineSimulator:
    """Generate synthetic pipeline inspection data."""

    def __init__(self, seed: int | None = None) -> None:
        """Initialize the simulator."""
        self._random = random.Random(seed)

    def generate_fault(
        self,
        length_m: float,
    ) -> SimulatedFault:
        """Generate a single simulated fault."""
        if length_m <= 0.0:
            raise ValueError("Pipeline length must be positive.")

        return SimulatedFault(
            fault_type=self._random.choice(
                [
                    "crack",
                    "corrosion",
                    "leak",
                ]
            ),
            position_m=self._random.uniform(
                0.0,
                length_m,
            ),
            confidence=round(
                self._random.uniform(
                    0.7,
                    0.99,
                ),
                3,
            ),
        )

    def generate_faults(
        self,
        length_m: float,
        count: int,
    ) -> list[SimulatedFault]:
        """Generate multiple simulated faults."""
        if count < 0:
            raise ValueError("count must be non-negative.")

        return [
            self.generate_fault(length_m)
            for _ in range(count)
        ]
