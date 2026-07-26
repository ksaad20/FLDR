"""FLDR - Fault Line Detection and Reporting Framework."""

from .pipeline import Pipeline
from .report import InspectionReport

__version__ = "0.0.1"
__author__ = "Asif Kazi"
__email__ = "kazisaadasif29@gmail.com"
__license__ = "Apache-2.0"

__all__ = [
    "Pipeline",
    "InspectionReport",
    "__version__",
]
