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

