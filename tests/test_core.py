"""Core unit tests for the FLDR package."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

import fldr


class TestPackageMetadata:
    """Tests for package-level metadata and exports."""

    def test_version_is_string(self) -> None:
        """Version should be a non-empty string."""
        assert isinstance(fldr.__version__, str)
        assert fldr.__version__.strip() != ""

    def test_version_matches_installed_package(self) -> None:
        """Package version should match the installed distribution, if available."""
        try:
            installed_version = version("fldr")
        except PackageNotFoundError:
            # Running directly from source without installation.
            assert isinstance(fldr.__version__, str)
            return

        assert fldr.__version__ == installed_version

    def test_author_is_string(self) -> None:
        """Author should be a non-empty string."""
        assert isinstance(fldr.__author__, str)
        assert fldr.__author__.strip() != ""

    def test_license_is_string(self) -> None:
        """License should be a non-empty string."""
        assert isinstance(fldr.__license__, str)
        assert fldr.__license__.strip() != ""

    def test_all_is_list_or_tuple(self) -> None:
        """__all__ should be a list or tuple."""
        assert isinstance(fldr.__all__, (list, tuple))

    def test_all_exports_are_strings(self) -> None:
        """Every export should be a string."""
        for export in fldr.__all__:
            assert isinstance(export, str)

    def test_all_exports_exist(self) -> None:
        """Every exported name should exist."""
        for export in fldr.__all__:
            assert hasattr(fldr, export), f"Missing export: {export}"


class TestPackageImports:
    """Tests for package import behavior."""

    def test_top_level_import_succeeds(self) -> None:
        """Top-level import should succeed."""
        assert fldr is not None

    def test_version_accessible_from_top_level(self) -> None:
        """Version should be accessible."""
        assert hasattr(fldr, "__version__")

    def test_author_accessible_from_top_level(self) -> None:
        """Author should be accessible."""
        assert hasattr(fldr, "__author__")

    def test_license_accessible_from_top_level(self) -> None:
        """License should be accessible."""
        assert hasattr(fldr, "__license__")

    def test_all_accessible_from_top_level(self) -> None:
        """__all__ should be accessible."""
        assert hasattr(fldr, "__all__")
