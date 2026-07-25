"""Shared pytest fixtures and configuration for FLDR test suite."""

from __future__ import annotations

import pytest


@pytest.fixture(scope="session")
def project_version() -> str:
    """Return the expected project version string."""
    return "0.1.0"


@pytest.fixture
def sample_data() -> dict[str, str]:
    """Return a sample dictionary for testing."""
    return {"key": "value", "foo": "bar"}


@pytest.fixture
def empty_collection() -> list:
    """Return an empty list for edge-case testing."""
    return []


@pytest.fixture
def invalid_inputs() -> list:
    """Return a list of common invalid inputs for parametrized tests."""
    return [None, "", [], {}, 0, -1, float("inf")]
  
