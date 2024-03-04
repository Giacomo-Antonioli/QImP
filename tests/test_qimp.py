"""Tests for `qimp` module."""
from typing import Generator

import pytest

import qimp


@pytest.fixture
def version() -> Generator[str, None, None]:
    """Sample pytest fixture."""
    yield qimp.__version__


def test_version(version: str) -> None:
    """Sample pytest test function with the pytest fixture as an argument."""
    assert version == "0.2.1"
