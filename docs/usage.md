# Usage Guide

This guide demonstrates the basic FLDR workflow.

The v0.0.1 release provides:

- Sensor signal simulation
- Fault detection
- Signal input/output utilities
- Reproducible experiments

---

## Basic Workflow

The typical FLDR workflow is:

```text
Generate Signal
       |
       v
Process Sensor Data
       |
       v
Detect Faults
       |
       v
Analyze Results

```
Import FLDR Components

from fldr.config import SimulationConfig
from fldr.simulation import FaultSimulator
from fldr.detector import FaultDetector

Configure a Simulation

Create a simulation configuration:

config = SimulationConfig(
    signal_length=1000,
    noise_level=0.1,
    num_faults=5,
    fault_amplitude=5.0,
    seed=42,
)

The configuration controls:

Signal length
Noise level
Number of injected faults
Fault amplitude
Random seed for reproducibility

Generate Synthetic Fault Data

Initialize the simulator:

simulator = FaultSimulator(config)

Generate a sensor signal:

data = simulator.generate()

The generated dataset contains:

Sensor signal values
Fault locations
Ground truth labels

Example:

signal = data["signal"]
labels = data["labels"]

Detect Faults

Initialize the detector:

detector = FaultDetector(
    threshold=3.0,
)

Run fault detection:

detections = detector.detect(signal)

The detector identifies signal regions that exceed the configured threshold.

Save and Load Signals

FLDR supports saving and loading sensor signals.

Import the IO utilities:

from fldr.io import save_signal, load_signal

Save a signal:

save_signal(
    signal,
    "sensor_data.npy",
)

Load a signal:

loaded_signal = load_signal(
    "sensor_data.npy",
)

Create:

docs/installation.md

# Installation

This guide explains how to install FLDR and prepare the development environment.

## Requirements

FLDR requires:

- Python 3.10 or newer
- pip package manager
- Git

Check your Python version:

```bash
python --version
Recommended:

Python 3.11+
Install from Source
Clone the repository:

git clone https://github.com/ksaad20/FLDR.git
Navigate into the project directory:

cd FLDR
Create a virtual environment:

python -m venv .venv
Activate the environment.

Linux/macOS
source .venv/bin/activate
Windows
.venv\Scripts\activate
Upgrade pip:

python -m pip install --upgrade pip
Install FLDR:

pip install -e .
Development Installation
For contributors and developers, install development dependencies:

pip install -e ".[dev]"
This installs:

Testing tools

Formatting tools

Linting tools

Coverage tools

Included tools:

pytest

pytest-cov

black

ruff

flake8

bandit

Verify Installation
Run:

python -c "import fldr; print('FLDR installation successful')"
Expected output:

FLDR installation successful
Run Tests
Verify the installation with:

pytest
For coverage:

pytest --cov=fldr
Code Quality Checks
Run formatting verification:

black --check --diff .
Run linting:

ruff check .
flake8 .
Troubleshooting
ModuleNotFoundError
If Python cannot find FLDR, reinstall the package:

pip install -e .
Make sure the virtual environment is activated.

Dependency Issues
Upgrade installed packages:

pip install --upgrade pip setuptools wheel
Then reinstall:

pip install -e ".[dev]"
Next Steps
After installation, continue with:

Usage Guide

Architecture Overview


This is appropriate for the v0.0.1 MVP documentation level: clear installation path, contributor setup, validation, and troubleshooting.

Now usage.md and architecture.md

Create:

docs/usage.md

# Usage Guide

This guide demonstrates the basic FLDR workflow.

The v0.0.1 release provides:

- Sensor signal simulation
- Fault detection
- Signal input/output utilities
- Reproducible experiments

---

## Basic Workflow

The typical FLDR workflow is:

```text
Generate Signal
       |
       v
Process Sensor Data
       |
       v
Detect Faults
       |
       v
Analyze Results
Import FLDR Components
from fldr.config import SimulationConfig
from fldr.simulation import FaultSimulator
from fldr.detector import FaultDetector
Generate a Synthetic Signal
Create a simulation configuration:

config = SimulationConfig(
    signal_length=1000,
    noise_level=0.1,
    num_faults=5,
    fault_amplitude=5.0,
    seed=42,
)
Initialize the simulator:

simulator = FaultSimulator(config)
Generate sensor data:

data = simulator.generate()
The generated output contains:

Sensor signal

Fault locations

Ground truth labels

Detect Faults
Initialize the detector:

detector = FaultDetector(
    threshold=3.0,
)
Run detection:

detections = detector.detect(
    data["signal"],
)
The detector returns fault predictions based on signal anomalies.

Saving and Loading Data
FLDR provides simple signal storage utilities:

from fldr.io import save_signal, load_signal
Save:

save_signal(
    data["signal"],
    "sample_signal.npy",
)
Load:

signal = load_signal(
    "sample_signal.npy",
)
Running Tests
Validate the installation:

pytest
Run with coverage:

pytest --cov=fldr
Current Limitations
The v0.0.1 release focuses on the core framework.

Future versions will add:

Advanced signal processing

Machine learning detectors

Multi-sensor fusion

Robotics integration

Real-world pipeline datasets


---

Create:

`docs/architecture.md`

```markdown id="x9k2fz"
