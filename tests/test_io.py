"""Tests for FLDR input/output utilities."""

from pathlib import Path

import numpy as np

from fldr.io import load_signal, save_signal


def test_save_signal_creates_file(tmp_path: Path):
    """Test saving a signal creates an output file."""
    signal = np.array([1.0, 2.0, 3.0])

    output_file = tmp_path / "signal.npy"

    save_signal(signal, output_file)

    assert output_file.exists()


def test_load_signal_returns_array(tmp_path: Path):
    """Test loading a saved signal returns numpy array."""
    signal = np.array([1.0, 2.0, 3.0])

    output_file = tmp_path / "signal.npy"

    save_signal(signal, output_file)

    loaded = load_signal(output_file)

    assert isinstance(loaded, np.ndarray)


def test_save_and_load_preserves_data(tmp_path: Path):
    """Test saved data matches loaded data."""
    signal = np.array(
        [0.5, -1.0, 4.2, 8.0],
    )

    output_file = tmp_path / "signal.npy"

    save_signal(signal, output_file)

    loaded = load_signal(output_file)

    np.testing.assert_array_equal(
        signal,
        loaded,
    )


def test_load_missing_file_raises_error(tmp_path: Path):
    """Test loading a missing file raises an error."""
    missing_file = tmp_path / "missing.npy"

    try:
        load_signal(missing_file)
    except FileNotFoundError:
        return

    raise AssertionError("Expected FileNotFoundError")
