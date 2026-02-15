"""Pytest fixtures for dashx tests."""
import os

import pytest


@pytest.fixture
def env_vars(monkeypatch):
    """Set DashX-related environment variables for tests."""
    monkeypatch.setenv("DASHX_PUBLIC_KEY", "test-public-key")
    monkeypatch.setenv("DASHX_PRIVATE_KEY", "test-private-key")
    monkeypatch.setenv("DASHX_TARGET_ENVIRONMENT", "test")
    monkeypatch.setenv("DASHX_BASE_URI", "https://api.dashx.com/graphql")


@pytest.fixture
def dashx_client(env_vars):
    """Return a DashX client with test env vars set."""
    from dashx import DashX
    return DashX()
