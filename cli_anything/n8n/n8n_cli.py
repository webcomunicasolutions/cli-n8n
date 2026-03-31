"""cli-anything-n8n — CLI for n8n workflow automation."""

from __future__ import annotations

import json
import sys
from typing import Any

import click

from cli_anything.n8n.core import (
    credentials,
    executions,
    project,
    tags,
    tables,
    variables,
    workflows,
)
from cli_anything.n8n.utils.repl_skin import error, output, print_banner, success


CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


def _conn(ctx: click.Context) -> dict[str, str]:
    """Extract connection kwargs from Click context."""
    return {"base_url": ctx.obj["base_url"], "api_key": ctx.obj["api_key"]}


def _json_flag(ctx: click.Context) -> bool:
    return ctx.obj.get("as_json", False)


def _load_json_arg(value: str) -> Any:
    """Parse a JSON string or read from file if prefixed with @."""
    if value.startswith("@"):
        with open(value[1:]) as f:
            return json.load(f)
    return json.loads(value)


# ─── Root ───────────────────────────────────────────────────────────────────

@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.option("--url", default=None, envvar="N8N_BASE_URL", help="n8n instance URL")
@click.option("--api-key", default=None, envvar="N8N_API_KEY", help="n8n API key")
@click.option("--json", "as_json", is_flag=True, default=False, help="JSON output")
@click.version_option(version="1.0.0", prog_name="cli-anything-n8n")
@click.pass_context
def cli(ctx: click.Context, url: str | None, api_key: str | None, as_json: bool) -> None:
    """CLI harness for n8n workflow automation."""
    ctx.ensure_object(dict)
    resolved_url, resolved_key = project.get_connection(url, api_key)
    ctx.obj["base_url"] = resolved_url
    ctx.obj["api_key"] = resolved_key
    ctx.obj["as_json"] = as_json
    if ctx.invoked_subcommand is None:
        ctx.invoke(repl)


# ─── REPL ───────────────────────────────────────────────────────────────────

@cli.command("repl", hidden=True)
@click.pass_context
def repl(ctx: click.Context) -> None:
    """Start interactive REPL."""
    try:
        from prompt_toolkit import PromptSession
        from prompt_toolkit.history import InMemoryHistory
    except ImportError:
        click.echo("prompt-toolkit is required for REPL mode. Install: pip install prompt-toolkit")
        sys.exit(1)

    base_url = ctx.obj["base_url"]
    print_banner(base_url or "(not configured)")

    session = PromptSession(history=InMemoryHistory())
    while True:
        try:
            line = session.prompt("n8n> ").strip()
        except (EOFError, KeyboardInterrupt):
            click.echo("\nBye!")
            break
        if not line:
            continue
        if line in ("exit", "quit", "q"):
            click.echo("Bye!")
            break
        if line == "help":
            click.echo(cli.get_help(ctx))
            continue
        try:
            args = line.split()
            cli.main(args, standalone_mode=False, obj=ctx.obj)
        except click.exceptions.UsageError as exc:
            error(str(exc))
        except SystemExit:
            pass
        except Exception as exc:
            error(str(exc))


# ─── Config ─────────────────────────────────────────────────────────────────

@cli.group("config")
def config_() -> None:
    """Configuration management."""


@config_.command("show")
@click.pass_context
def config_show(ctx: click.Context) -> None:
    """Show current configuration."""
    cfg = project.load_config()
    # Mask the API key for display
    masked = {**cfg}
    if masked.get("api_key"):
        key = masked["api_key"]
        masked["api_key"] = f"{key[:4]}...{key[-4:]}" if len(key) > 8 else "****"
    output(masked, _json_flag(ctx))


@config_.command("set")
@click.argument("key")
@click.argument("value")
@click.pass_context
def config_set(ctx: click.Context, key: str, value: str) -> None:
    """Set a config value (base_url, api_key)."""
    cfg = project.load_config()
    if key not in ("base_url", "api_key"):
        error(f"Unknown config key: {key}. Use: base_url, api_key")
        return
    cfg[key] = value
    path = project.save_config(cfg)
    success(f"Saved {key} to {path}")


# ─── Workflows ──────────────────────────────────────────────────────────────

@cli.group("workflow")
def workflow_() -> None:
    """Workflow management."""


@workflow_.command("list")
@click.option("--active/--inactive", default=None, help="Filter by active status")
@click.option("--tags", "tag_filter", default=None, help="Filter by tag names (comma-separated)")
@click.option("--name", default=None, help="Filter by name (contains)")
@click.option("--limit", default=50, type=int, help="Max results")
@click.option("--cursor", default=None, help="Pagination cursor")
@click.pass_context
def workflow_list(ctx: click.Context, active: bool | None, tag_filter: str | None, name: str | None, limit: int, cursor: str | None) -> None:
    """List workflows."""
    data = workflows.list_workflows(
        **_conn(ctx), active=active, tags=tag_filter, name=name, limit=limit, cursor=cursor,
    )
    output(data, _json_flag(ctx))


@workflow_.command("get")
@click.argument("workflow_id")
@click.pass_context
def workflow_get(ctx: click.Context, workflow_id: str) -> None:
    """Get workflow details."""
    data = workflows.get_workflow(workflow_id, **_conn(ctx))
    output(data, _json_flag(ctx))


@workflow_.command("create")
@click.argument("json_data")
@click.pass_context
def workflow_create(ctx: click.Context, json_data: str) -> None:
    """Create a workflow from JSON (inline or @file.json)."""
    data = workflows.create_workflow(_load_json_arg(json_data), **_conn(ctx))
    output(data, _json_flag(ctx))


@workflow_.command("update")
@click.argument("workflow_id")
@click.argument("json_data")
@click.pass_context
def workflow_update(ctx: click.Context, workflow_id: str, json_data: str) -> None:
    """Update a workflow."""
    data = workflows.update_workflow(workflow_id, _load_json_arg(json_data), **_conn(ctx))
    output(data, _json_flag(ctx))


@workflow_.command("delete")
@click.argument("workflow_id")
@click.confirmation_option(prompt="Are you sure you want to delete this workflow?")
@click.pass_context
def workflow_delete(ctx: click.Context, workflow_id: str) -> None:
    """Delete a workflow."""
    workflows.delete_workflow(workflow_id, **_conn(ctx))
    success(f"Workflow {workflow_id} deleted")


@workflow_.command("activate")
@click.argument("workflow_id")
@click.pass_context
def workflow_activate(ctx: click.Context, workflow_id: str) -> None:
    """Activate a workflow."""
    data = workflows.activate_workflow(workflow_id, **_conn(ctx))
    output(data, _json_flag(ctx))


@workflow_.command("deactivate")
@click.argument("workflow_id")
@click.pass_context
def workflow_deactivate(ctx: click.Context, workflow_id: str) -> None:
    """Deactivate a workflow."""
    data = workflows.deactivate_workflow(workflow_id, **_conn(ctx))
    output(data, _json_flag(ctx))


@workflow_.command("tags")
@click.argument("workflow_id")
@click.pass_context
def workflow_tags(ctx: click.Context, workflow_id: str) -> None:
    """Get workflow tags."""
    data = workflows.get_workflow_tags(workflow_id, **_conn(ctx))
    output(data, _json_flag(ctx))


# ─── Executions ─────────────────────────────────────────────────────────────

@cli.group("execution")
def execution_() -> None:
    """Execution management."""


@execution_.command("list")
@click.option("--status", type=click.Choice(["error", "success", "waiting", "running", "new"]), default=None)
@click.option("--workflow-id", default=None, help="Filter by workflow ID")
@click.option("--limit", default=20, type=int)
@click.option("--cursor", default=None)
@click.option("--include-data", is_flag=True, default=False, help="Include execution data")
@click.pass_context
def execution_list(ctx: click.Context, status: str | None, workflow_id: str | None, limit: int, cursor: str | None, include_data: bool) -> None:
    """List executions."""
    data = executions.list_executions(
        **_conn(ctx), status=status, workflow_id=workflow_id, limit=limit, cursor=cursor, include_data=include_data,
    )
    output(data, _json_flag(ctx))


@execution_.command("get")
@click.argument("execution_id")
@click.option("--no-data", is_flag=True, default=False, help="Exclude execution data")
@click.pass_context
def execution_get(ctx: click.Context, execution_id: str, no_data: bool) -> None:
    """Get execution details."""
    data = executions.get_execution(execution_id, **_conn(ctx), include_data=not no_data)
    output(data, _json_flag(ctx))


@execution_.command("delete")
@click.argument("execution_id")
@click.pass_context
def execution_delete(ctx: click.Context, execution_id: str) -> None:
    """Delete an execution."""
    executions.delete_execution(execution_id, **_conn(ctx))
    success(f"Execution {execution_id} deleted")


@execution_.command("retry")
@click.argument("execution_id")
@click.pass_context
def execution_retry(ctx: click.Context, execution_id: str) -> None:
    """Retry a failed execution."""
    data = executions.retry_execution(execution_id, **_conn(ctx))
    output(data, _json_flag(ctx))


@execution_.command("stop")
@click.argument("execution_id")
@click.pass_context
def execution_stop(ctx: click.Context, execution_id: str) -> None:
    """Stop a running execution."""
    data = executions.stop_execution(execution_id, **_conn(ctx))
    output(data, _json_flag(ctx))


# ─── Credentials ────────────────────────────────────────────────────────────

@cli.group("credential")
def credential_() -> None:
    """Credential management."""


@credential_.command("list")
@click.pass_context
def credential_list(ctx: click.Context) -> None:
    """List credentials."""
    data = credentials.list_credentials(**_conn(ctx))
    output(data, _json_flag(ctx))


@credential_.command("create")
@click.argument("json_data")
@click.pass_context
def credential_create(ctx: click.Context, json_data: str) -> None:
    """Create a credential from JSON."""
    data = credentials.create_credential(_load_json_arg(json_data), **_conn(ctx))
    output(data, _json_flag(ctx))


@credential_.command("update")
@click.argument("credential_id")
@click.argument("json_data")
@click.pass_context
def credential_update(ctx: click.Context, credential_id: str, json_data: str) -> None:
    """Update a credential."""
    data = credentials.update_credential(credential_id, _load_json_arg(json_data), **_conn(ctx))
    output(data, _json_flag(ctx))


@credential_.command("delete")
@click.argument("credential_id")
@click.confirmation_option(prompt="Are you sure you want to delete this credential?")
@click.pass_context
def credential_delete(ctx: click.Context, credential_id: str) -> None:
    """Delete a credential."""
    credentials.delete_credential(credential_id, **_conn(ctx))
    success(f"Credential {credential_id} deleted")


@credential_.command("schema")
@click.argument("credential_type")
@click.pass_context
def credential_schema(ctx: click.Context, credential_type: str) -> None:
    """Get credential schema for a type."""
    data = credentials.get_credential_schema(credential_type, **_conn(ctx))
    output(data, _json_flag(ctx))


# ─── Variables ──────────────────────────────────────────────────────────────

@cli.group("variable")
def variable_() -> None:
    """Variable management."""


@variable_.command("list")
@click.pass_context
def variable_list(ctx: click.Context) -> None:
    """List all variables."""
    data = variables.list_variables(**_conn(ctx))
    output(data, _json_flag(ctx))


@variable_.command("create")
@click.argument("key")
@click.argument("value")
@click.pass_context
def variable_create(ctx: click.Context, key: str, value: str) -> None:
    """Create a variable."""
    data = variables.create_variable(key, value, **_conn(ctx))
    output(data, _json_flag(ctx))


@variable_.command("update")
@click.argument("variable_id")
@click.argument("key")
@click.argument("value")
@click.pass_context
def variable_update(ctx: click.Context, variable_id: str, key: str, value: str) -> None:
    """Update a variable."""
    data = variables.update_variable(variable_id, key, value, **_conn(ctx))
    output(data, _json_flag(ctx))


@variable_.command("delete")
@click.argument("variable_id")
@click.pass_context
def variable_delete(ctx: click.Context, variable_id: str) -> None:
    """Delete a variable."""
    variables.delete_variable(variable_id, **_conn(ctx))
    success(f"Variable {variable_id} deleted")


# ─── Tags ───────────────────────────────────────────────────────────────────

@cli.group("tag")
def tag_() -> None:
    """Tag management."""


@tag_.command("list")
@click.option("--limit", default=50, type=int)
@click.pass_context
def tag_list(ctx: click.Context, limit: int) -> None:
    """List all tags."""
    data = tags.list_tags(**_conn(ctx), limit=limit)
    output(data, _json_flag(ctx))


@tag_.command("get")
@click.argument("tag_id")
@click.pass_context
def tag_get(ctx: click.Context, tag_id: str) -> None:
    """Get tag details."""
    data = tags.get_tag(tag_id, **_conn(ctx))
    output(data, _json_flag(ctx))


@tag_.command("create")
@click.argument("name")
@click.pass_context
def tag_create(ctx: click.Context, name: str) -> None:
    """Create a tag."""
    data = tags.create_tag(name, **_conn(ctx))
    output(data, _json_flag(ctx))


@tag_.command("update")
@click.argument("tag_id")
@click.argument("name")
@click.pass_context
def tag_update(ctx: click.Context, tag_id: str, name: str) -> None:
    """Update a tag name."""
    data = tags.update_tag(tag_id, name, **_conn(ctx))
    output(data, _json_flag(ctx))


@tag_.command("delete")
@click.argument("tag_id")
@click.pass_context
def tag_delete(ctx: click.Context, tag_id: str) -> None:
    """Delete a tag."""
    tags.delete_tag(tag_id, **_conn(ctx))
    success(f"Tag {tag_id} deleted")


# ─── Data Tables ────────────────────────────────────────────────────────────

@cli.group("table")
def table_() -> None:
    """Data Table management."""


@table_.command("list")
@click.option("--limit", default=50, type=int)
@click.pass_context
def table_list(ctx: click.Context, limit: int) -> None:
    """List data tables."""
    data = tables.list_tables(**_conn(ctx), limit=limit)
    output(data, _json_flag(ctx))


@table_.command("get")
@click.argument("table_id")
@click.pass_context
def table_get(ctx: click.Context, table_id: str) -> None:
    """Get table details."""
    data = tables.get_table(table_id, **_conn(ctx))
    output(data, _json_flag(ctx))


@table_.command("create")
@click.argument("name")
@click.option("--columns", default=None, help="Columns as JSON array")
@click.pass_context
def table_create(ctx: click.Context, name: str, columns: str | None) -> None:
    """Create a data table."""
    cols = json.loads(columns) if columns else None
    data = tables.create_table(name, cols, **_conn(ctx))
    output(data, _json_flag(ctx))


@table_.command("delete")
@click.argument("table_id")
@click.confirmation_option(prompt="Are you sure you want to delete this table?")
@click.pass_context
def table_delete(ctx: click.Context, table_id: str) -> None:
    """Delete a data table."""
    tables.delete_table(table_id, **_conn(ctx))
    success(f"Table {table_id} deleted")


@table_.command("rows")
@click.argument("table_id")
@click.option("--limit", default=50, type=int)
@click.option("--cursor", default=None)
@click.pass_context
def table_rows(ctx: click.Context, table_id: str, limit: int, cursor: str | None) -> None:
    """Query rows from a data table."""
    data = tables.query_rows(table_id, **_conn(ctx), limit=limit, cursor=cursor)
    output(data, _json_flag(ctx))


@table_.command("insert")
@click.argument("table_id")
@click.argument("json_data")
@click.pass_context
def table_insert(ctx: click.Context, table_id: str, json_data: str) -> None:
    """Insert rows into a data table (JSON array or @file.json)."""
    data = tables.insert_rows(table_id, _load_json_arg(json_data), **_conn(ctx))
    output(data, _json_flag(ctx))


@table_.command("update-rows")
@click.argument("table_id")
@click.argument("json_data")
@click.pass_context
def table_update_rows(ctx: click.Context, table_id: str, json_data: str) -> None:
    """Update rows in a data table."""
    data = tables.update_rows(table_id, _load_json_arg(json_data), **_conn(ctx))
    output(data, _json_flag(ctx))


# ─── Entry point ────────────────────────────────────────────────────────────

def main() -> None:
    cli(obj={})


if __name__ == "__main__":
    main()
