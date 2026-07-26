"""
Basic FLDR simulation example.

This example demonstrates how to:
- Configure a synthetic fault experiment
- Generate sensor data
- Inspect generated outputs
"""

from fldr.config import SimulationConfig
from fldr.simulation import FaultSimulator


def main() -> None:
    """Run a basic FLDR simulation."""
    config = SimulationConfig(
        signal_length=1000,
        noise_level=0.1,
        num_faults=5,
        fault_amplitude=5.0,
        seed=42,
    )

    simulator = FaultSimulator(config)

    data = simulator.generate()

    signal = data["signal"]
    labels = data["labels"]

    print("FLDR simulation completed")
    print(f"Signal samples: {len(signal)}")
    print(f"Detected fault samples in ground truth: {labels.sum()}")


if __name__ == "__main__":
    main()
