"""E2E tests — require a running n8n instance.

Set N8N_BASE_URL and N8N_API_KEY env vars to run these tests.
Skip with: pytest -m "not e2e"
"""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

from cli_anything.n8n.core import tags, variables, workflows


pytestmark = pytest.mark.e2e

N8N_URL = os.environ.get("N8N_BASE_URL", "")
N8N_KEY = os.environ.get("N8N_API_KEY", "")


def _skip_if_no_n8n():
    if not N8N_URL or not N8N_KEY:
        pytest.skip("N8N_BASE_URL and N8N_API_KEY required for E2E tests")


def _resolve_cli() -> list[str]:
    """Find the CLI binary or fall back to python -m."""
    import shutil
    if shutil.which("cli-anything-n8n"):
        return ["cli-anything-n8n"]
    return [sys.executable, "-m", "cli_anything.n8n"]


# ─── Subprocess tests (no n8n needed) ──────────────────────────────────────

class TestCLISubprocess:
    def test_help(self):
        result = subprocess.run(
            [*_resolve_cli(), "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "n8n workflow automation" in result.stdout

    def test_version(self):
        result = subprocess.run(
            [*_resolve_cli(), "--version"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "1.0.0" in result.stdout

    def test_workflow_help(self):
        result = subprocess.run(
            [*_resolve_cli(), "workflow", "--help"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        assert "list" in result.stdout

    def test_config_show_json(self):
        result = subprocess.run(
            [*_resolve_cli(), "--json", "config", "show"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0


# ─── E2E tests (n8n required) ──────────────────────────────────────────────

class TestWorkflowsE2E:
    def test_list_workflows(self):
        _skip_if_no_n8n()
        result = workflows.list_workflows(base_url=N8N_URL, api_key=N8N_KEY, limit=5)
        assert "data" in result

    def test_workflow_crud(self):
        """Create, get, update, delete — without activate (requires trigger node)."""
        _skip_if_no_n8n()
        import requests as req

        # Create
        wf = workflows.create_workflow(
            {"name": "CLI-Anything Test WF", "nodes": [], "connections": {}, "settings": {}},
            base_url=N8N_URL, api_key=N8N_KEY,
        )
        wf_id = wf["id"]

        try:
            # Get
            detail = workflows.get_workflow(wf_id, base_url=N8N_URL, api_key=N8N_KEY)
            assert detail["name"] == "CLI-Anything Test WF"

            # Update — send only the fields n8n accepts
            updated = workflows.update_workflow(
                wf_id,
                {"name": "CLI-Anything Test WF Updated", "nodes": [], "connections": {}, "settings": {}},
                base_url=N8N_URL, api_key=N8N_KEY,
            )
            assert updated["name"] == "CLI-Anything Test WF Updated"
        finally:
            # Cleanup
            workflows.delete_workflow(wf_id, base_url=N8N_URL, api_key=N8N_KEY)

        # Verify deletion — should 404
        try:
            workflows.get_workflow(wf_id, base_url=N8N_URL, api_key=N8N_KEY)
            assert False, "Workflow should have been deleted"
        except req.exceptions.HTTPError as e:
            assert e.response.status_code == 404


class TestVariablesE2E:
    def test_list_variables(self):
        """Variables API may require Enterprise license — skip on 403."""
        _skip_if_no_n8n()
        import requests
        try:
            result = variables.list_variables(base_url=N8N_URL, api_key=N8N_KEY)
            assert isinstance(result, (list, dict))
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                pytest.skip("Variables API requires Enterprise license")
            raise


class TestTagsE2E:
    def test_list_tags(self):
        _skip_if_no_n8n()
        result = tags.list_tags(base_url=N8N_URL, api_key=N8N_KEY)
        assert isinstance(result, (list, dict))

    def test_tag_lifecycle(self):
        _skip_if_no_n8n()
        import uuid
        unique_name = f"CLITEST{uuid.uuid4().hex[:8].upper()}"

        # Create
        tag = tags.create_tag(unique_name, base_url=N8N_URL, api_key=N8N_KEY)
        tag_id = tag["id"]

        try:
            # List and verify
            all_tags = tags.list_tags(base_url=N8N_URL, api_key=N8N_KEY)
            data = all_tags.get("data", all_tags) if isinstance(all_tags, dict) else all_tags
            names = [t["name"] for t in data if isinstance(t, dict)]
            assert unique_name in names

            # Update
            updated_name = f"{unique_name}UPD"
            updated = tags.update_tag(tag_id, updated_name, base_url=N8N_URL, api_key=N8N_KEY)
            assert updated["name"] == updated_name
        finally:
            # Cleanup
            tags.delete_tag(tag_id, base_url=N8N_URL, api_key=N8N_KEY)
