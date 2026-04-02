# cli-anything-n8n

[![PyPI](https://img.shields.io/pypi/v/cli-anything-n8n.svg)](https://pypi.org/project/cli-anything-n8n/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![CLI-Anything](https://img.shields.io/badge/CLI--Anything-harness-orange.svg)](https://github.com/HKUDS/CLI-Anything)
[![n8n API v1.1.1](https://img.shields.io/badge/n8n-API%20v1.1.1-EA4B71.svg)](https://docs.n8n.io/api/api-reference/)

> **66 commands** | **94 tests** | **38 security fixes** | **7 review rounds**
>
> [Leer en Español](#español) | [Read in English](#english)

---

<a id="english"></a>

## English

### Why this project exists

Control your [n8n](https://n8n.io) instance from the terminal — **without needing an MCP server**.

If you use **Claude Code** (or any AI coding agent) and want to manage n8n workflows, the typical approach is an MCP server. But MCPs consume context window, require IDE-specific config, and aren't portable. This CLI takes a simpler approach:

```
# With MCP (complex, IDE-specific):
AI Agent -> MCP Server -> n8n API

# With cli-anything-n8n (universal, zero config):
AI Agent -> shell -> cli-anything-n8n -> n8n API
```

Built with [Claude Code](https://claude.ai/code) using the [CLI-Anything](https://github.com/HKUDS/CLI-Anything) pattern. Verified against the real **n8n OpenAPI spec v1.1.1** (n8n 2.43.0). Hardened through **7 rounds of adversarial security review** (38 fixes).

### Install (30 seconds)

```bash
pip install cli-anything-n8n

export N8N_BASE_URL=https://your-n8n.com
export N8N_API_KEY=your-api-key    # Settings > API > Create API Key

cli-anything-n8n workflow list
```

### All 66 commands

#### Workflow management (25 commands)

| Command | What it does |
|---------|-------------|
| `workflow list` | List workflows (filter: --active, --tags, --name) |
| `workflow search "text"` | Search by name (case-insensitive) |
| `workflow get ID` | Get workflow details |
| `workflow create @file.json` | Create from JSON file |
| `workflow update ID @file.json` | Update (auto-snapshots before changes) |
| `workflow delete ID` | Delete (with confirmation) |
| `workflow activate ID` | Activate a workflow |
| `workflow deactivate ID` | Deactivate a workflow |
| `workflow tags ID` | Get workflow tags |
| `workflow set-tags ID '[{"id":"..."}]'` | Set tags |
| `workflow transfer ID PROJECT_ID` | Transfer to another project |
| `workflow export ID` | Export to portable JSON file |
| `workflow import file.json` | Import from file (always inactive) |
| `workflow backup-all` | Backup ALL workflows to a folder |
| `workflow restore-all ./backup/` | Restore from backup (--dry-run) |
| `workflow diff ID1 ID2` | Compare two workflows (colored diff) |
| `workflow bulk-activate --tag X` | Activate multiple by tag/name |
| `workflow bulk-deactivate --search X` | Deactivate multiple by tag/name |
| `workflow validate ID` | Check structure, connections, triggers |
| `workflow autofix ID` | Detect and repair common issues (--apply) |
| `workflow patch ID --rename "New Name"` | Incremental changes (rename, enable/disable/remove nodes, connect/disconnect) |
| `workflow test ID` | Trigger webhook with test data |
| `workflow scaffold webhook --deploy` | Generate from pattern (webhook, api, database, ai-agent, scheduled) |
| `workflow patterns` | List available scaffold patterns |
| `workflow versions list/rollback/diff/prune/show/stats` | Version history with rollback |

#### Execution management (6 commands)

| Command | What it does |
|---------|-------------|
| `execution list` | List executions (--status error/success/running) |
| `execution get ID` | Get details (--no-data for lightweight) |
| `execution delete ID` | Delete an execution |
| `execution retry ID` | Retry a failed execution |
| `execution errors` | Quick view of recent failures (--details) |
| `execution watch` | Live monitoring (--interval 5 --workflow-id X) |

#### Templates from n8n.io (3 commands)

| Command | What it does |
|---------|-------------|
| `template search "telegram bot"` | Search 2,700+ templates |
| `template get 7756` | View template details |
| `template deploy 7756` | Deploy directly to your n8n |

#### Community nodes via npm (2 commands)

| Command | What it does |
|---------|-------------|
| `node search "stripe"` | Search 26,000+ node packages |
| `node info n8n-nodes-telegram` | Package details + install command |

#### Credential management (4 commands)

| Command | What it does |
|---------|-------------|
| `credential create @cred.json` | Create a credential |
| `credential delete ID` | Delete (with confirmation) |
| `credential schema httpBasicAuth` | Get schema for a type |
| `credential transfer ID PROJECT_ID` | Transfer to project |

#### Variable management (4 commands)

| Command | What it does |
|---------|-------------|
| `variable list` | List all variables |
| `variable create KEY VALUE` | Create |
| `variable update ID KEY VALUE` | Update |
| `variable delete ID` | Delete |

#### Tag management (5 commands)

| Command | What it does |
|---------|-------------|
| `tag list` | List all tags |
| `tag get ID` | Get details |
| `tag create "name"` | Create |
| `tag update ID "new name"` | Update |
| `tag delete ID` | Delete |

#### Configuration and tools (7 commands)

| Command | What it does |
|---------|-------------|
| `config show` | Show config (API key always masked) |
| `config set base_url https://...` | Save connection |
| `config test` | Verify n8n connectivity |
| `status` | Dashboard: workflows, executions, errors |
| `health --diagnostic` | Instance health + response time |
| `expression "={{$json.name}}"` | Validate n8n expression syntax |
| `completions bash\|zsh\|fish` | Shell tab-completion |

### For AI agents

```bash
cli-anything-n8n --json workflow list
cli-anything-n8n --json execution errors --details
cli-anything-n8n workflow create @workflow.json
```

All commands support `--json` for machine-readable output. Exit code 0 = success.

### Security

- 7 rounds of adversarial review (38 fixes)
- API key never exposed in any output
- File permissions restricted (0600/0700)
- All imported/restored/deployed workflows forced inactive
- SQLite WAL mode + timeout for concurrent access
- Webhook URLs sanitized
- npm data validated and truncated

### n8n compatibility

Verified against **n8n 2.43.0** (API v1.1.1). Works with n8n >= 1.0.0.

### Development

```bash
git clone https://github.com/webcomunicasolutions/cli-n8n.git
cd cli-n8n
pip install -e . && pip install pytest
pytest cli_anything/n8n/tests/ -v
```

### License

MIT - [Juan Jose Sanchez Bernal](mailto:info@webcomunica.solutions) / [Webcomunica Soluciones Informaticas](https://webcomunica.solutions)

---

<a id="español"></a>

## Español

### Por que existe

Controla tu instancia [n8n](https://n8n.io) desde la terminal — **sin necesitar un servidor MCP**.

Si usas **Claude Code** y quieres gestionar workflows de n8n, normalmente necesitas un MCP. Pero los MCPs consumen contexto, requieren configuracion por IDE, y no son portables. Este CLI es mas simple:

```
# Con MCP (complejo, especifico por IDE):
Agente IA -> Servidor MCP -> API n8n

# Con cli-anything-n8n (universal, sin config):
Agente IA -> shell -> cli-anything-n8n -> API n8n
```

Construido con [Claude Code](https://claude.ai/code). Verificado contra la **especificacion OpenAPI real** de n8n 2.43.0. Endurecido con **7 rondas de revision adversarial** (38 fixes).

### Instalar (30 segundos)

```bash
pip install cli-anything-n8n

export N8N_BASE_URL=https://tu-n8n.com
export N8N_API_KEY=tu-api-key    # Settings > API > Create API Key

cli-anything-n8n workflow list
```

### 66 comandos

| Grupo | Comandos | Destacados |
|-------|----------|------------|
| **workflow** (25) | list, search, get, create, update, delete, activate, deactivate, tags, set-tags, transfer, export, import, backup-all, restore-all, diff, bulk-activate, bulk-deactivate, validate, autofix, patch, test, scaffold, patterns, versions | Backup/restore, diff, autofix, scaffolds, rollback |
| **execution** (6) | list, get, delete, retry, errors, watch | Monitoreo en vivo, troubleshooting |
| **template** (3) | search, get, deploy | 2,700+ templates de n8n.io |
| **node** (2) | search, info | 26,000+ paquetes npm |
| **credential** (4) | create, delete, schema, transfer | |
| **variable** (4) | list, create, update, delete | |
| **tag** (5) | list, get, create, update, delete | |
| **config** (3) | show, set, test | |
| **tools** (4) | status, health, expression, completions | Dashboard, diagnostico, validador |

### Seguridad

- 7 rondas de revision adversarial (38 fixes)
- API key nunca expuesta
- Workflows importados/restaurados/deployados siempre inactivos
- SQLite WAL + timeout
- Datos de npm validados y truncados

### Licencia

MIT - [Juan Jose Sanchez Bernal](mailto:info@webcomunica.solutions) / [Webcomunica Soluciones Informaticas](https://webcomunica.solutions)
