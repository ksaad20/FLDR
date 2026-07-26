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
# Architecture Overview

FLDR is designed as a modular fault detection framework for robotic inspection and sensor-based monitoring systems.

---

## High-Level Architecture

```text
                    FLDR Framework

+--------------------------------+
|          User Interface        |
|       CLI / Python API         |
+----------------+---------------+
                 |
                 v
+--------------------------------+
|        Processing Layer        |
|                                |
|  Simulation     Input/Output   |
|                                |
+----------------+---------------+
                 |
                 v
+--------------------------------+
|       Detection Layer          |
|                                |
|  FaultDetector                 |
|  RuleBasedDetector             |
|                                |
+----------------+---------------+
                 |
                 v
+--------------------------------+
|        Results Layer           |
|                                |
| DetectionResult                |
| Evaluation Metrics             |
+--------------------------------+
Core Modules
config.py
Responsible for configuration management.

Provides:

Simulation parameters

Detector settings

Experiment reproducibility

Main component:

SimulationConfig
simulation.py
Provides synthetic sensor data generation.

Responsibilities:

Generate normal signals

Inject fault events

Produce labelled datasets

Used for:

Algorithm testing

Benchmark development

CI validation

detector.py
Contains fault detection algorithms.

Current components:

FaultDetector
Baseline threshold-based detector.

Purpose:

Establish initial detection pipeline

Provide simple reproducible baseline

BaseDetector
Abstract interface for future detectors.

Allows implementations such as:

Machine learning models

Deep learning architectures

Physics-informed methods

RuleBasedDetector
Initial rule-based detection framework.

Future extensions:

Sensor fusion rules

Domain-specific fault logic

Expert systems

io.py
Handles data persistence.

Provides:

Signal saving

Signal loading

Current format:

NumPy binary (.npy)
Data Flow
Sensor Data
     |
     v
Input Layer
     |
     v
Preprocessing
     |
     v
Detection Algorithm
     |
     v
Fault Results
     |
     v
Analysis
Design Principles
FLDR follows these principles:

Modularity
Each component has a defined responsibility.

Reproducibility
Experiments use configurable parameters and deterministic random seeds.

Extensibility
New detection algorithms can be added without modifying the core framework.

Open Science
Testing, documentation, and automated workflows are included from the beginning.

Future Architecture
Planned extensions include:

                Advanced FLDR

+-----------------------------+
| Robotic Inspection Platform |
+-------------+---------------+
              |
              v
+-----------------------------+
| Multi-Sensor Data Fusion    |
+-------------+---------------+
              |
              v
+-----------------------------+
| AI/ML Fault Detection       |
+-------------+---------------+
              |
              v
+-----------------------------+
| Digital Twin + Analytics    |
+-----------------------------+
The v0.0.1 architecture provides the foundation for these future capabilities.


With these three docs:

- ✅ `index.md`
- ✅ `installation.md`
- ✅ `usage.md`
- ✅ `architecture.md`

your MkDocs documentation structure is ready for an MVP release.

Generate usage.md

Create:

docs/usage.md

# Usage Guide

This guide demonstrates the basic FLDR workflow for generating sensor data and detecting faults.

The v0.0.1 release provides:

- Synthetic fault signal generation
- Baseline fault detection
- Signal input/output utilities
- Reproducible experiments

---

## Basic Workflow

A typical FLDR workflow:

```text
Configure Experiment
        |
        v
Generate or Load Sensor Data
        |
        v
Run Fault Detection
        |
        v
Analyze Detection Results
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
Complete Example
The complete workflow:

from fldr.config import SimulationConfig
from fldr.simulation import FaultSimulator
from fldr.detector import FaultDetector


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

results = detector.detect(
    data["signal"],
)

print(results)
Running FLDR Tests
Validate the installation:

pytest
Run with coverage:

pytest --cov=fldr
Development Checks
Before contributing, run:

black --check --diff .
ruff check .
flake8 .
Current Scope
FLDR v0.0.1 focuses on establishing a reliable foundation:

Simulation framework

Detection interfaces

Reproducible testing

Extensible architecture

Future releases will expand toward:

Advanced signal processing

Machine learning-based detection

Multi-sensor fusion

Robotic inspection workflows

Real-world pipeline datasets

