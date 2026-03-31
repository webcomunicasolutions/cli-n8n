---
name: cli-anything-n8n
description: >-
  Command-line interface for n8n workflow automation platform.
  Manages workflows, executions, credentials, variables, tags, and data tables.
---

# cli-anything-n8n

CLI harness for n8n workflow automation — built with the CLI-Anything pattern.

## Installation

```bash
pip install cli-anything-n8n
```

## Configuration

```bash
# Set connection (persisted to ~/.cli-anything/n8n/config.json)
cli-anything-n8n config set base_url https://your-n8n-instance.com
cli-anything-n8n config set api_key your-api-key

# Or use environment variables
export N8N_BASE_URL=https://your-n8n-instance.com
export N8N_API_KEY=your-api-key
```

## Usage

### CLI Mode

```bash
cli-anything-n8n workflow list
cli-anything-n8n workflow get 123
cli-anything-n8n execution list --status error --limit 10
cli-anything-n8n variable create MY_VAR "my value"
```

### REPL Mode

```bash
cli-anything-n8n  # starts interactive REPL
n8n> workflow list
n8n> execution list --status error
n8n> exit
```

## Command Groups

| Group       | Commands                                         |
|-------------|--------------------------------------------------|
| workflow    | list, get, create, update, delete, activate, deactivate, tags |
| execution   | list, get, delete, retry, stop                   |
| credential  | list, create, update, delete, schema             |
| variable    | list, create, update, delete                     |
| tag         | list, get, create, update, delete                |
| table       | list, get, create, delete, rows, insert, update-rows |
| config      | show, set                                        |

## Output Formats

- **Human-readable**: default, with colored tables
- **JSON**: `--json` flag for machine-parseable output

## For AI Agents

- Always use `--json` flag for structured output
- Check return codes: 0 = success, non-zero = error
- Use `@file.json` to pass complex JSON from files
- Workflow IDs are strings, not integers
- Use `config set` to persist connection details
