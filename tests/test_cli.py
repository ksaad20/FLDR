"""Tests for the FLDR command-line interface."""

from __future__ import annotations

from typer.testing import CliRunner

from fldr.cli import app

runner = CliRunner()


class TestCLI:
    """Tests for the command-line interface."""

    def test_cli_invokes(self) -> None:
        """CLI should execute successfully."""
        result = runner.invoke(app)
        assert result.exit_code == 0

    def test_help_option(self) -> None:
        """Help option should display usage information."""
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "Usage" in result.stdout

    def test_version_option(self) -> None:
        """Version option should execute successfully."""
        result = runner.invoke(app, ["--version"])

        assert result.exit_code == 0

    def test_cli_output_is_string(self) -> None:
        """CLI output should be text."""
        result = runner.invoke(app)

        assert isinstance(result.stdout, str)
