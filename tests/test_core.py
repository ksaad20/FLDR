"""Core unit tests for the FLDR package."""

from __future__ import annotations

import fldr


class TestPackageMetadata:
    """Tests for package-level metadata and exports."""

    def test_version_is_string(self) -> None:
        """Version should be a string."""
        assert isinstance(fldr.__version__, str)

    def test_version_matches_expected(self, project_version: str) -> None:
        """Version should match the expected value."""
        assert fldr.__version__ == project_version

    def test_author_is_string(self) -> None:
        """Author should be a string."""
        assert isinstance(fldr.__author__, str)

    def test_license_is_string(self) -> None:
        """License should be a string."""
        assert isinstance(fldr.__license__, str)

    def test_all_exports_are_strings(self) -> None:
        """All exports in __all__ should be strings."""
        for export in fldr.__all__:
            assert isinstance(export, str)

    def test_all_exports_exist(self) -> None:
        """Every name in __all__ should be accessible on the package."""
        for export in fldr.__all__:
            assert hasattr(fldr, export)


class TestPackageImports:
    """Tests for package import behavior."""

    def test_top_level_import_succeeds(self) -> None:
        """Importing the top-level package should succeed."""
        import fldr as _fldr  # noqa: F401

    def test_version_accessible_from_top_level(self) -> None:
        """Version should be accessible from the top-level namespace."""
        assert hasattr(fldr, "__version__")
