"""CLI smoke tests for FLDR."""

from __future__ import annotations

import importlib


class TestCLI:
    """Smoke tests for the CLI module."""

    def test_cli_module_imports(self) -> None:
        """The CLI module should import successfully."""
        module = importlib.import_module("fldr.cli")
        assert module is not None

    def test_cli_module_has_public_attributes(self) -> None:
        """The CLI module should define at least one public attribute."""
        module = importlib.import_module("fldr.cli")
        public = [name for name in dir(module) if not name.startswith("_")]

        assert public
