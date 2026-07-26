"""Command-line interface for FLDR."""

from __future__ import annotations

import typer

app = typer.Typer(help="FLDR command-line interface.")


@app.command()
def version() -> None:
    """Print the package version."""
    from fldr import __version__

    typer.echo(__version__)


if __name__ == "__main__":
    app()
