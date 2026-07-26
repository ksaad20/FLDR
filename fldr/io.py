"""Input/output utilities for FLDR."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any
import numpy as np

from fldr.core import InspectionReport


def save_signal(
    signal: np.ndarray,
    path: str | Path,
) -> None:
    """
    Save a sensor signal to disk.

    Parameters
    ----------
    signal:
        One-dimensional sensor signal.
    path:
        Output file path.
    """
    output_path = Path(path)

    np.save(
        output_path,
        signal,
    )


def load_signal(
    path: str | Path,
) -> np.ndarray:
    """
    Load a sensor signal from disk.

    Parameters
    ----------
    path:
        Input file path.

    Returns
    -------
    np.ndarray
        Loaded sensor signal.
    """
    input_path = Path(path)

    return np.load(input_path)


def save_report_json(report: InspectionReport, path: str | Path) -> Path:
    """Save an inspection report as JSON."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as file:
        json.dump(report.to_dict(), file, indent=2)

    return output


def load_report_json(path: str | Path) -> dict[str, Any]:
    """Load a JSON report."""
    report_path = Path(path)

    with report_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_results_csv(report: InspectionReport, path: str | Path) -> Path:
    """Save detection results as CSV."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                "fault_type",
                "confidence",
                "position_m",
            ]
        )

        for result in report.results:
            writer.writerow(
                [
                    result.fault_type,
                    result.confidence,
                    result.position_m,
                ]
            )

    return output


def ensure_directory(path: str | Path) -> Path:
    """Create a directory if it does not already exist."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def file_exists(path: str | Path) -> bool:
    """Return True if a file exists."""
    return Path(path).is_file()
