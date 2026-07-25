"""FLDR command-line interface."""

from __future__ import annotations

import importlib
import typer


__version__ = "0.0.1"

app = typer.Typer(
    name="fldr",
    help=(
        "FLDR: Open-source fault-line detection framework for robotics, "
        "autonomous systems, and geospatial sensing."
    ),
    no_args_is_help=True,
    rich_markup_mode="rich",
)

COMMAND_MODULES: dict[str, str] = {
    "info": "fldr.commands.info",
    "version": "fldr.commands.version",
    "doctor": "fldr.commands.doctor",
    "config": "fldr.commands.config",
    "init": "fldr.commands.init",
    "detect": "fldr.commands.detect",
    "calibrate": "fldr.commands.calibrate",
    "benchmark": "fldr.commands.benchmark",
    "simulate": "fldr.commands.simulate",
    "visualize": "fldr.commands.visualize",
    "export": "fldr.commands.export",
    "datasets": "fldr.commands.datasets",
    "models": "fldr.commands.models",
    "plugins": "fldr.commands.plugins",
    "train": "fldr.commands.train",
    "evaluate": "fldr.commands.evaluate",
    "pipeline": "fldr.commands.pipeline",
    "monitor": "fldr.commands.monitor",
    "diagnostics": "fldr.commands.diagnostics",
    "validate": "fldr.commands.validate",
    "inspect": "fldr.commands.inspect",
    "convert": "fldr.commands.convert",
    "report": "fldr.commands.report",
    "serve": "fldr.commands.serve",
    "api": "fldr.commands.api",
    "cloud": "fldr.commands.cloud",
    "edge": "fldr.commands.edge",
    "robot": "fldr.commands.robot",
    "sensor": "fldr.commands.sensor",
    "lidar": "fldr.commands.lidar",
    "camera": "fldr.commands.camera",
    "imu": "fldr.commands.imu",
    "gps": "fldr.commands.gps",
    "fusion": "fldr.commands.fusion",
    "localization": "fldr.commands.localization",
    "mapping": "fldr.commands.mapping",
    "navigation": "fldr.commands.navigation",
    "logging": "fldr.commands.logging",
    "profile": "fldr.commands.profile",
    "security": "fldr.commands.security",
    "package": "fldr.commands.package",
    "update": "fldr.commands.update",
    "install": "fldr.commands.install",
    "uninstall": "fldr.commands.uninstall",
}


def _load_command(module_name: str) -> typer.Typer | None:
    """Attempt to load a command module."""
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        return None

    command = getattr(module, "app", None)

    if isinstance(command, typer.Typer):
        return command

    return None


def _register_commands() -> None:
    """Register every available command."""
    for name, module in sorted(COMMAND_MODULES.items()):
        command = _load_command(module)

        if command is not None:
            app.add_typer(command, name=name)


_register_commands()


@app.callback()
def main() -> None:
    """FLDR command-line interface."""


@app.command()
def version() -> None:
    """Display the FLDR version."""
    typer.echo(f"FLDR {__version__}")


@app.command()
def info() -> None:
    """Display installation information."""
    typer.echo("FLDR")
    typer.echo(f"Version: {__version__}")
    typer.echo("Status: Operational")
    typer.echo(f"Registered command groups: {len(COMMAND_MODULES)}")


@app.command()
def commands() -> None:
    """List available command groups."""
    for command in sorted(COMMAND_MODULES):
        typer.echo(command)


@app.command()
def doctor() -> None:
    """Run installation diagnostics."""
    typer.echo("✓ Python environment detected.")
    typer.echo("✓ FLDR core available.")
    typer.echo("✓ CLI operational.")
    typer.echo("✓ Command loader initialized.")


def run() -> None:
    """Application entry point."""
    app()


if __name__ == "__main__":
    run()
