# Changelog

## [2.1.3] - 2026-04-01

### Security Fixes (review round 2 — security agent)
- **Path traversal**: 3 additional file reads in diff/validate/autofix now use centralized `_load_json_arg()` with `Path.resolve()`
- **Webhook URL sanitization**: Strip special chars from webhook path to prevent URL manipulation
- **Error message leaking**: Removed raw server response from error output

## [2.1.2] - 2026-04-01

### Fixes (from review round 2)
- **SQLite race condition**: Added WAL journal mode + 10s timeout for concurrent access
- **Filename encoding**: Safe filename sanitization for workflows with unicode/special chars
- **Watch busy-loop**: Reject `--interval 0` to prevent CPU burn
- **Duplicate dict key**: Removed duplicate `api_key_set` in health diagnostic
- **Versions diff same**: Warn when comparing version with itself
- Added `_safe_filename()` helper for cross-platform filename safety

## [2.1.1] - 2026-04-01

### Security Fixes (from 3-agent code review)
- **Path traversal prevention**: `_load_json_arg()` now resolves paths before opening
- **API key no longer exposed**: `health --diagnostic` shows only "configured/NOT SET"
- **File permissions**: config.json (0600) and versions.db directory (0700) are now restricted
- **Specific exceptions**: Replaced bare `except Exception: pass` with targeted exception types

### Code Quality Fixes
- Extracted `_clean_for_api()` helper — eliminated 7 duplicated filter expressions
- Added `_INTERNAL_FIELDS` constant for workflow metadata fields
- Fixed `versions_diff` missing `@click.pass_context` decorator
- Fixed `_iter_params` to detect expressions inside lists (not just dicts)
- Reviewed by: code-reviewer, security-reviewer, python-reviewer agents

## [2.1.0] - 2026-04-01

### Added
- `node search <query>` — search 26,000+ n8n community node packages on npm
- `node info <package>` — get package details, nodes provided, install command
- New module: `core/nodes.py`

## [2.0.0] - 2026-04-01

### Added
- `workflow scaffold <pattern>` — generate workflows from 5 proven patterns (webhook, api, database, ai-agent, scheduled)
- `workflow patterns` — list available scaffold patterns
- `expression <expr>` — validate n8n expression syntax offline
- New modules: `core/scaffolds.py`, `core/expressions.py`

### Changed
- Version bump to 2.0.0 — the CLI is now feature-complete for the n8n Public API
- 10 core modules, 60+ commands, 80+ tests

## [1.7.0] - 2026-04-01

### Added
- `workflow versions list/show/rollback/diff/prune/stats` — full version tracking with local SQLite
- Auto-snapshot before every write operation (update, patch, autofix --apply)
- Rollback to any previous version with automatic pre-rollback backup
- Version diff between any two stored snapshots
- Storage stats and pruning for disk management

## [1.6.0] - 2026-04-01

### Added
- `workflow autofix` — detect and repair 6 types of common issues (expression format, webhook paths, broken connections, duplicate names, numeric connection keys, unused error outputs). Preview mode by default.
- `workflow patch` — incremental updates: `--rename`, `--enable-node`, `--disable-node`, `--remove-node`, `--connect`, `--disconnect`. No need to send the full workflow JSON.
- `health` — full health check with response time, connectivity test, and `--diagnostic` mode
- New module `core/fixers.py` with pluggable fix engine

### Inspired by
- `WorkflowAutoFixer` and `WorkflowDiffEngine` from [n8n-mcp](https://github.com/czlonkowski/n8n-mcp)

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
