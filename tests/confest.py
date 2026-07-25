"""Core unit tests for the FLDR package."""

from __future__ import annotations

import fldr


class TestPackageMetadata:
    """Tests for package metadata."""

    def test_version_exists(self) -> None:
        """Version should exist and be a non-empty string."""
        assert hasattr(fldr, "__version__")
        assert isinstance(fldr.__version__, str)
        assert fldr.__version__.strip()

    def test_author_exists(self) -> None:
        """Author should exist and be a non-empty string."""
        assert hasattr(fldr, "__author__")
        assert isinstance(fldr.__author__, str)
        assert fldr.__author__.strip()

    def test_license_exists(self) -> None:
        """License should exist and be a non-empty string."""
        assert hasattr(fldr, "__license__")
        assert isinstance(fldr.__license__, str)
        assert fldr.__license__.strip()

    def test_all_exists(self) -> None:
        """__all__ should exist."""
        assert hasattr(fldr, "__all__")
        assert isinstance(fldr.__all__, (list, tuple))

    def test_all_exports_are_strings(self) -> None:
        """Every export should be a string."""
        for export in fldr.__all__:
            assert isinstance(export, str)

    def test_all_exports_exist(self) -> None:
        """Every exported name should exist."""
        for export in fldr.__all__:
            assert hasattr(fldr, export), (
                f"Missing exported attribute: {export}"
            )


class TestPackageImports:
    """Tests for importing the package."""

    def test_import(self) -> None:
        """Top-level import should succeed."""
        assert fldr is not None

    def test_top_level_version(self) -> None:
        """Version should be accessible."""
        assert hasattr(fldr, "__version__")

    def test_top_level_author(self) -> None:
        """Author should be accessible."""
        assert hasattr(fldr, "__author__")

    def test_top_level_license(self) -> None:
        """License should be accessible."""
        assert hasattr(fldr, "__license__")
