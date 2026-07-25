"""Shared pytest fixtures for the FLDR test suite."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def project_version() -> str:
    """
    Return the installed project version.

    Falls back to '0.1.0' when running directly from source without an
    installed package.
    """
    try:
        return version("fldr")
    except PackageNotFoundError:
        return "0.1.0"


@pytest.fixture(scope="session")
def package_name() -> str:
    """Return the package name."""
    return "fldr"


@pytest.fixture(scope="session")
def expected_author() -> str:
    """Expected package author."""
    return "FLDR Development Team"


@pytest.fixture(scope="session")
def expected_license() -> str:
    """Expected package license."""
    return "Apache-2.0"


@pytest.fixture(scope="session")
def random_seed() -> int:
    """Deterministic random seed."""
    return 42
