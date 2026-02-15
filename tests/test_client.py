"""Tests for the DashX client."""
import os
from unittest.mock import patch, MagicMock

import pytest

from dashx import DashX


class TestDashXInit:
    """Tests for DashX initialization and configuration."""

    def test_init_uses_env_vars(self, env_vars):
        client = DashX()
        assert client.public_key == "test-public-key"
        assert client.private_key == "test-private-key"
        assert client.target_environment == "test"
        assert client.base_uri == "https://api.dashx.com/graphql"

    def test_init_explicit_keys_override_env(self, env_vars):
        client = DashX(
            public_key="explicit-public",
            private_key="explicit-private",
            target_environment="staging",
        )
        assert client.public_key == "explicit-public"
        assert client.private_key == "explicit-private"
        assert client.target_environment == "staging"

    def test_init_raises_without_public_key(self, monkeypatch):
        monkeypatch.delenv("DASHX_PUBLIC_KEY", raising=False)
        monkeypatch.setenv("DASHX_PRIVATE_KEY", "sk")
        monkeypatch.setenv("DASHX_TARGET_ENVIRONMENT", "test")
        with pytest.raises(ValueError, match="Public key is required"):
            DashX()

    def test_init_raises_without_private_key(self, monkeypatch):
        monkeypatch.setenv("DASHX_PUBLIC_KEY", "pk")
        monkeypatch.delenv("DASHX_PRIVATE_KEY", raising=False)
        monkeypatch.setenv("DASHX_TARGET_ENVIRONMENT", "test")
        with pytest.raises(ValueError, match="Private key is required"):
            DashX()

    def test_init_raises_without_target_environment(self, monkeypatch):
        monkeypatch.setenv("DASHX_PUBLIC_KEY", "pk")
        monkeypatch.setenv("DASHX_PRIVATE_KEY", "sk")
        monkeypatch.delenv("DASHX_TARGET_ENVIRONMENT", raising=False)
        with pytest.raises(ValueError, match="Target environment is required"):
            DashX()

    def test_init_default_base_uri_without_env(self, monkeypatch):
        monkeypatch.delenv("DASHX_BASE_URI", raising=False)
        monkeypatch.setenv("DASHX_PUBLIC_KEY", "pk")
        monkeypatch.setenv("DASHX_PRIVATE_KEY", "sk")
        monkeypatch.setenv("DASHX_TARGET_ENVIRONMENT", "test")
        client = DashX()
        assert client.base_uri == "https://api.dashx.com/graphql"

    def test_init_custom_base_uri_from_env(self, monkeypatch):
        monkeypatch.setenv("DASHX_BASE_URI", "https://custom.dashx.com/graphql")
        monkeypatch.setenv("DASHX_PUBLIC_KEY", "pk")
        monkeypatch.setenv("DASHX_PRIVATE_KEY", "sk")
        monkeypatch.setenv("DASHX_TARGET_ENVIRONMENT", "test")
        client = DashX()
        assert client.base_uri == "https://custom.dashx.com/graphql"


class TestGenerateHeader:
    """Tests for request header generation."""

    def test_generate_header_includes_all_keys(self, dashx_client):
        headers = dashx_client.generate_header()
        assert headers["User-Agent"] == "dashx-python"
        assert headers["Content-Type"] == "application/json"
        assert headers["X-Public-Key"] == "test-public-key"
        assert headers["X-Private-Key"] == "test-private-key"
        assert headers["X-Target-Environment"] == "test"


class TestIdentify:
    """Tests for identify method."""

    @patch("dashx.client.DashX._execute")
    def test_identify_with_uid_calls_execute(self, mock_execute, dashx_client):
        mock_execute.return_value = {"identifyAccount": {"id": "123"}}
        dashx_client.identify(uid="user-123")
        mock_execute.assert_called_once()
        variables = mock_execute.call_args[0][1]
        assert variables["input"]["uid"] == "user-123"

    @patch("dashx.client.DashX._execute")
    def test_identify_without_uid_uses_anonymous_uid(self, mock_execute, dashx_client):
        mock_execute.return_value = {"identifyAccount": {"id": "anon-1"}}
        dashx_client.identify()
        mock_execute.assert_called_once()
        variables = mock_execute.call_args[0][1]
        assert "anonymousUid" in variables["input"]
        assert len(variables["input"]["anonymousUid"]) == 36  # UUID format

    @patch("dashx.client.DashX._execute")
    def test_identify_passes_extra_params(self, mock_execute, dashx_client):
        mock_execute.return_value = {"identifyAccount": {"id": "123"}}
        dashx_client.identify(uid="user-1", email="u@example.com")
        variables = mock_execute.call_args[0][1]
        assert variables["input"]["uid"] == "user-1"
        assert variables["input"]["email"] == "u@example.com"


class TestTrack:
    """Tests for track method."""

    @patch("dashx.client.DashX._execute")
    def test_track_with_uid_calls_execute(self, mock_execute, dashx_client):
        mock_execute.return_value = {"trackEvent": {"success": True}}
        dashx_client.track(event="purchase", uid="user-123", data={"amount": 99})
        mock_execute.assert_called_once()
        variables = mock_execute.call_args[0][1]
        assert variables["input"]["event"] == "purchase"
        assert variables["input"]["accountUid"] == "user-123"
        assert variables["input"]["data"] == {"amount": 99}

    @patch("dashx.client.DashX._execute")
    def test_track_without_uid_uses_anonymous_uid(self, mock_execute, dashx_client):
        mock_execute.return_value = {"trackEvent": {"success": True}}
        dashx_client.track(event="page_view")
        variables = mock_execute.call_args[0][1]
        assert "accountAnonymousUid" in variables["input"]
        assert variables["input"]["event"] == "page_view"
        assert len(variables["input"]["accountAnonymousUid"]) == 36
