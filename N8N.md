# N8N.md — Architecture

## Overview

`cli-anything-n8n` wraps the n8n REST API into a Click-based CLI, following the CLI-Anything harness pattern by HKUDS.

## Architecture

```
cli_anything/n8n/
├── n8n_cli.py          # Click CLI (groups, commands, REPL)
├── core/               # Business logic (thin wrappers over backend)
│   ├── workflows.py    # 11 endpoints
│   ├── executions.py   # 8 endpoints
│   ├── credentials.py  # 6 endpoints
│   ├── variables.py    # 4 endpoints
│   ├── tags.py         # 5 endpoints
│   ├── tables.py       # 10 endpoints
│   ├── project.py      # Config load/save
│   └── session.py      # REPL state
├── utils/
│   ├── n8n_backend.py  # HTTP client (sole module making requests)
│   └── repl_skin.py    # Banner, colors, table formatting
├── skills/
│   └── SKILL.md        # AI agent discovery
└── tests/
    ├── test_core.py    # Unit tests (mocked)
    └── test_full_e2e.py # E2E tests (live n8n)
```

## Data Flow

```
User/Agent → n8n_cli.py (Click) → core/*.py → n8n_backend.py → n8n REST API
```

## Authentication

Header-based: `X-N8N-API-KEY: <key>`

Resolution order: CLI arg `--api-key` > env `N8N_API_KEY` > config file

## Conventions

- All core functions accept `base_url` and `api_key` as keyword args
- All commands support `--json` for parseable output
- PEP 420 namespace: `cli_anything/` has NO `__init__.py`
- Entry point: `cli-anything-n8n` → `cli_anything.n8n.n8n_cli:main`
