"""Data Tables management — CRUD tables + CRUD rows."""

from __future__ import annotations

from typing import Any

from cli_anything.n8n.utils.n8n_backend import (
    api_delete,
    api_get,
    api_post,
    api_put,
)


# --- Tables ---

def list_tables(*, base_url: str | None = None, api_key: str | None = None, limit: int = 50) -> Any:
    return api_get("/data-tables", base_url=base_url, api_key=api_key, params={"limit": limit})


def get_table(table_id: str, *, base_url: str | None = None, api_key: str | None = None) -> Any:
    return api_get(f"/data-tables/{table_id}", base_url=base_url, api_key=api_key)


def create_table(name: str, columns: list[dict[str, Any]] | None = None, *, base_url: str | None = None, api_key: str | None = None) -> Any:
    data: dict[str, Any] = {"name": name}
    if columns:
        data["columns"] = columns
    return api_post("/data-tables", data, base_url=base_url, api_key=api_key)


def delete_table(table_id: str, *, base_url: str | None = None, api_key: str | None = None) -> Any:
    return api_delete(f"/data-tables/{table_id}", base_url=base_url, api_key=api_key)


# --- Rows ---

def query_rows(
    table_id: str,
    *,
    base_url: str | None = None,
    api_key: str | None = None,
    limit: int = 50,
    cursor: str | None = None,
    filters: dict[str, Any] | None = None,
) -> Any:
    params: dict[str, Any] = {"limit": limit}
    if cursor:
        params["cursor"] = cursor
    if filters:
        params.update(filters)
    return api_get(f"/data-tables/{table_id}/rows", base_url=base_url, api_key=api_key, params=params)


def insert_rows(table_id: str, rows: list[dict[str, Any]], *, base_url: str | None = None, api_key: str | None = None) -> Any:
    return api_post(f"/data-tables/{table_id}/rows", rows, base_url=base_url, api_key=api_key)


def update_rows(table_id: str, rows: list[dict[str, Any]], *, base_url: str | None = None, api_key: str | None = None) -> Any:
    return api_put(f"/data-tables/{table_id}/rows", rows, base_url=base_url, api_key=api_key)


def upsert_rows(table_id: str, rows: list[dict[str, Any]], *, base_url: str | None = None, api_key: str | None = None) -> Any:
    return api_post(f"/data-tables/{table_id}/rows/upsert", rows, base_url=base_url, api_key=api_key)


def delete_rows(table_id: str, row_ids: list[str], *, base_url: str | None = None, api_key: str | None = None) -> Any:
    return api_post(f"/data-tables/{table_id}/rows/delete", {"ids": row_ids}, base_url=base_url, api_key=api_key)
