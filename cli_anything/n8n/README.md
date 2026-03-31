# cli-anything-n8n

CLI harness for [n8n](https://n8n.io) workflow automation — built with the [CLI-Anything](https://github.com/HKUDS/CLI-Anything) pattern.

## Features

- Full n8n REST API coverage: workflows, executions, credentials, variables, tags, data tables
- Interactive REPL mode with colored output
- JSON output for AI agent consumption (`--json`)
- Config persistence (`~/.cli-anything/n8n/config.json`)
- PEP 420 namespace packaging — coexists with other CLI-Anything harnesses

## Quick Start

```bash
pip install cli-anything-n8n

# Configure
export N8N_BASE_URL=https://your-n8n.example.com
export N8N_API_KEY=your-api-key

# Use
cli-anything-n8n workflow list
cli-anything-n8n --json execution list --status error
```

## Development

```bash
cd agent-harness
pip install -e .
pytest cli_anything/n8n/tests/test_core.py -v
```

## License

MIT
