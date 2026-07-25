"""Core unit tests for the FLDR package."""

from __future__ import annotations

import fldr


class TestPackageMetadata:
    """Tests for package-level metadata."""

    def test_version_exists(self) -> None:
        """The package should define a version string."""
        assert hasattr(fldr, "__version__")
        assert isinstance(fldr.__version__, str)
        assert fldr.__version__.strip()

    def test_author_exists(self) -> None:
        """The package should define an author string."""
        assert hasattr(fldr, "__author__")
        assert isinstance(fldr.__author__, str)
        assert fldr.__author__.strip()

    def test_license_exists(self) -> None:
        """The package should define a license string."""
        assert hasattr(fldr, "__license__")
        assert isinstance(fldr.__license__, str)
        assert fldr.__license__.strip()

    def test_all_exists(self) -> None:
        """The package should define __all__."""
        assert hasattr(fldr, "__all__")
        assert isinstance(fldr.__all__, (list, tuple))

    def test_all_exports_are_strings(self) -> None:
        """Every exported symbol should be a string."""
        for export in fldr.__all__:
            assert isinstance(export, str)

    def test_all_exports_exist(self) -> None:
        """Every exported symbol should exist."""
        for export in fldr.__all__:
            assert hasattr(
                fldr,
                export,
            ), f"Missing exported attribute: {export}"


class TestPackageImports:
    """Tests for package import behavior."""

    def test_import_succeeds(self) -> None:
        """Importing the package should succeed."""
        assert fldr is not None

    def test_version_accessible(self) -> None:
        """Version should be accessible."""
        assert hasattr(fldr, "__version__")

    def test_author_accessible(self) -> None:
        """Author should be accessible."""
        assert hasattr(fldr, "__author__")

    def test_license_accessible(self) -> None:
        """License should be accessible."""
        assert hasattr(fldr, "__license__")

    def test_all_accessible(self) -> None:
        """__all__ should be accessible."""
        assert hasattr(fldr, "__all__")
