# Changelog

## [1.5.0] - 2026-04-01

### Added
- `template search <query>` — search 2,700+ templates on n8n.io
- `template get <id>` — view template details
- `template deploy <id>` — deploy template directly to your n8n instance
- `workflow validate <id|@file>` — validate workflow structure (nodes, connections, triggers, duplicates)
- `workflow test <id>` — trigger webhook-based workflows with test data

### Inspired by
- Features from [n8n-mcp](https://github.com/czlonkowski/n8n-mcp) adapted for CLI usage

## [1.4.0] - 2026-04-01

### Added
- `workflow backup-all` — backup ALL workflows to a folder (disaster recovery)
- `workflow restore-all` — restore workflows from a backup folder (with `--dry-run`)
- `workflow diff` — compare two workflows or a workflow vs a local file (colored diff)
- `execution errors` — quick view of recent failures with optional `--details`

## [1.3.0] - 2026-04-01

### Added
- `config test` — verify your n8n connection works before doing anything
- `workflow search <query>` — find workflows by name (case-insensitive)
- `workflow bulk-activate --tag X` / `--search X` — activate multiple workflows at once
- `workflow bulk-deactivate --tag X` / `--search X` — deactivate multiple workflows at once
- `completions bash|zsh|fish` — generate shell completion scripts
- Colored status/active columns in table output (green=success, red=error, etc.)

## [1.2.0] - 2026-04-01

### Added
- `workflow export` — save any workflow to a portable JSON file
- `workflow import` — create a workflow from a JSON file (with optional name override)
- `execution watch` — live monitoring of executions with real-time polling
- `status` — dashboard showing workflows, recent executions, and errors at a glance
- REPL tab-completion for all commands and subcommands
- GitHub Actions CI (Python 3.10-3.13)

## [1.1.0] - 2026-03-31

### Changed
- **BREAKING**: Removed `credential list` and `credential update` commands (not supported by n8n Public API v1.1.1)
- **BREAKING**: Removed `execution stop` command (not in public API)
- **BREAKING**: Removed `table` command group (Data Tables not in public API v1.1.1)
- Aligned all endpoints with verified n8n OpenAPI spec v1.1.1
- Version bumped to 1.1.0

### Added
- `workflow set-tags` command to update workflow tags
- `workflow transfer` command to transfer workflows between projects
- `credential transfer` command to transfer credentials between projects
- URL validation in `config set base_url`
- Configurable timeout via `N8N_TIMEOUT` env var (default: 30s)
- Ellipsis indicator when table columns are truncated
- Better JSON error messages (`@file.json` not found, invalid JSON)

### Fixed
- `credential list` no longer crashes with 405 (command removed — API doesn't support it)
- `_load_json_arg` now shows clear error for missing files and invalid JSON
- API key is always masked in `config show`, even with `--json`

### Removed
- `setup.py` (replaced by `pyproject.toml`)
- `core/session.py` (unused REPL state dataclass)
- `core/tables.py` (Data Tables not in n8n Public API)
- `execution stop/stop-all` (not in public API)
- `execution tags/set-tags` (not in public API)

## [1.0.0] - 2026-03-31

### Added
- Initial release
- CLI harness following CLI-Anything pattern
- Workflow management (list, get, create, update, delete, activate, deactivate, tags)
- Execution management (list, get, delete, retry)
- Credential management (create, delete, schema)
- Variable management (CRUD)
- Tag management (CRUD)
- Interactive REPL mode with colored output
- JSON output mode (`--json`)
- Config persistence (`~/.cli-anything/n8n/config.json`)
- 29 unit tests, E2E test suite
