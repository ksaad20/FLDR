"""
Basic FLDR fault detection example.

This example demonstrates:
- Configuring a simulation
- Generating synthetic sensor data
- Running fault detection
- Reporting detected fault locations
"""

from fldr.config import SimulationConfig
from fldr.detector import FaultDetector
from fldr.simulation import FaultSimulator


def main() -> None:
    """Run a basic FLDR fault detection workflow."""
    config = SimulationConfig(
        signal_length=1000,
        noise_level=0.1,
        num_faults=5,
        fault_amplitude=5.0,
        seed=42,
    )

    simulator = FaultSimulator(config)

    data = simulator.generate()

    detector = FaultDetector(
        threshold=3.0,
    )

    detections = detector.detect(
        data["signal"],
    )

    fault_count = int(sum(detections))

    print("FLDR fault detection completed")
    print(f"Signal samples: {len(data['signal'])}")
    print(f"Detected fault samples: {fault_count}")

    if fault_count > 0:
        locations = [
            index
            for index, value in enumerate(detections)
            if value == 1
        ]

        print(f"First detected fault locations: {locations[:10]}")
    else:
        print("No faults detected")


if __name__ == "__main__":
    main()
