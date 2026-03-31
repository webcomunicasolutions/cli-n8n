"""Credential management — CRUD, schema, transfer."""

from __future__ import annotations

from typing import Any

from cli_anything.n8n.utils.n8n_backend import (
    api_delete,
    api_get,
    api_patch,
    api_post,
    api_put,
)


def list_credentials(*, base_url: str | None = None, api_key: str | None = None) -> Any:
    return api_get("/credentials", base_url=base_url, api_key=api_key)


def create_credential(data: dict[str, Any], *, base_url: str | None = None, api_key: str | None = None) -> Any:
    return api_post("/credentials", data, base_url=base_url, api_key=api_key)


def update_credential(credential_id: str, data: dict[str, Any], *, base_url: str | None = None, api_key: str | None = None) -> Any:
    return api_patch(f"/credentials/{credential_id}", data, base_url=base_url, api_key=api_key)


def delete_credential(credential_id: str, *, base_url: str | None = None, api_key: str | None = None) -> Any:
    return api_delete(f"/credentials/{credential_id}", base_url=base_url, api_key=api_key)


def get_credential_schema(credential_type: str, *, base_url: str | None = None, api_key: str | None = None) -> Any:
    return api_get(f"/credentials/schema/{credential_type}", base_url=base_url, api_key=api_key)


def transfer_credential(credential_id: str, project_id: str, *, base_url: str | None = None, api_key: str | None = None) -> Any:
    return api_put(f"/credentials/{credential_id}/transfer", {"destinationProjectId": project_id}, base_url=base_url, api_key=api_key)
