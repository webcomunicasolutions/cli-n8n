# cli-anything-n8n

[![PyPI](https://img.shields.io/pypi/v/cli-anything-n8n.svg)](https://pypi.org/project/cli-anything-n8n/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![CLI-Anything](https://img.shields.io/badge/CLI--Anything-harness-orange.svg)](https://github.com/HKUDS/CLI-Anything)
[![n8n API v1.1.1](https://img.shields.io/badge/n8n-API%20v1.1.1-EA4B71.svg)](https://docs.n8n.io/api/api-reference/)

> [Leer en Español](#español) | [Read in English](#english)

---

<a id="english"></a>

## English

### Why this project exists

If you use **[Claude Code](https://claude.ai/code)** (or any AI coding agent) and want to manage your **[n8n](https://n8n.io)** workflows, you typically need an **MCP server** — a special integration that connects the AI to n8n's API. MCP servers work, but they have limitations:

- They consume context window (every tool definition eats tokens)
- They require specific configuration per IDE/client
- They're not portable — you can't use them outside Claude Code
- They add a layer of complexity between the AI and the API

**cli-anything-n8n** takes a different approach: it's a **standard CLI tool** that any AI agent can use through regular shell commands. No MCP needed. No special integration. Just `pip install` and go.

```
# With MCP (complex setup, IDE-specific):
Claude Code -> MCP Server -> n8n API

# With cli-anything-n8n (universal, zero config):
Claude Code -> shell -> cli-anything-n8n -> n8n API
Any AI agent -> shell -> cli-anything-n8n -> n8n API
You -> terminal -> cli-anything-n8n -> n8n API
```

### How it was built

This project was built entirely with **Claude Code** in a single session:

1. **Research** — Analyzed the [CLI-Anything](https://github.com/HKUDS/CLI-Anything) framework (25k+ stars) and the n8n REST API
2. **API verification** — Downloaded the actual OpenAPI spec from a live n8n 2.43.0 instance (`/api/v1/openapi.yml`) to verify which endpoints really exist in the public API
3. **Implementation** — Built the full CLI following the CLI-Anything pattern: Click commands, HTTP client, REPL mode, colored output
4. **Testing** — 44 automated tests (33 unit + 11 E2E against real n8n)
5. **Publication** — Published to [PyPI](https://pypi.org/project/cli-anything-n8n/) and submitted a [PR to CLI-Anything](https://github.com/HKUDS/CLI-Anything/pull/171)

Only verified, working endpoints are exposed. Many n8n features (Data Tables, credential listing, execution stop) are **not** in the public API — we don't pretend they work.

### Try it now (2 minutes)

```bash
# 1. Install
pip install cli-anything-n8n

# 2. Connect to your n8n
export N8N_BASE_URL=https://your-n8n-instance.com
export N8N_API_KEY=your-api-key

# 3. Use it
cli-anything-n8n workflow list
cli-anything-n8n --json execution list --status error
cli-anything-n8n tag create "production"
```

> **Where do I get my API key?** In n8n, go to Settings > API > Create API Key.

### Using with Claude Code (or any AI agent)

The `--json` flag makes output machine-readable. Any AI agent that can run shell commands can use this:

```bash
# Claude Code can run these directly:
cli-anything-n8n --json workflow list
cli-anything-n8n --json workflow get ABC123
cli-anything-n8n --json execution list --status error --limit 5
cli-anything-n8n workflow create @workflow.json
```

No MCP configuration needed. No tool definitions eating your context window. Just shell commands.

### Interactive REPL mode

```bash
cli-anything-n8n
n8n> workflow list --active
n8n> execution list --status error
n8n> tag list
n8n> exit
```

### All commands

| Group | Commands | What it does |
|-------|----------|--------------|
| **workflow** | list, get, create, update, delete, activate, deactivate, tags, set-tags, transfer, **export**, **import** | Manage your workflows |
| **execution** | list, get, delete, retry, **watch** | Check, retry, and monitor executions |
| **credential** | create, delete, schema, transfer | Manage credentials |
| **variable** | list, create, update, delete | Manage environment variables |
| **tag** | list, get, create, update, delete | Organize with tags |
| **config** | show, set | Save your connection settings |

### Export and import workflows

Move workflows between n8n instances or keep backups:

```bash
# Export a workflow to a JSON file
cli-anything-n8n workflow export ABC123
# -> saves "My_Workflow.json"

# Export with custom filename
cli-anything-n8n workflow export ABC123 -o backup.json

# Import into another instance
cli-anything-n8n workflow import backup.json

# Import with a new name
cli-anything-n8n workflow import backup.json --name "Copy of My Workflow"
```

### Status dashboard

See everything at a glance:

```bash
cli-anything-n8n status
```

```
  n8n Status Dashboard
  ========================================

  Workflows
    Total:    42
    Active:   15
    Inactive: 27

  Recent Executions (last 10)
    180357   success   wf:cLUnUzjQGfAClPNC  2026-03-31 20:24:00
    180356   success   wf:cLUnUzjQGfAClPNC  2026-03-31 20:23:30
    180355   error     wf:ABC123             2026-03-31 20:23:00

  Errors: 1 in last 10 executions
    Last error: execution 180355 (wf:ABC123) at 2026-03-31 20:23:0
```

### Watch executions live

Monitor your n8n in real-time:

```bash
# Watch all executions (updates every 5 seconds)
cli-anything-n8n execution watch

# Watch a specific workflow
cli-anything-n8n execution watch --workflow-id ABC123

# Custom interval
cli-anything-n8n execution watch --interval 10
```

### Save your connection

```bash
cli-anything-n8n config set base_url https://your-n8n-instance.com
cli-anything-n8n config set api_key your-api-key

# Now just use it directly
cli-anything-n8n workflow list
```

### Configuration

| Method | Priority | Example |
|--------|----------|---------|
| CLI flags | 1 (highest) | `--url https://... --api-key xxx` |
| Environment variables | 2 | `N8N_BASE_URL`, `N8N_API_KEY` |
| Config file | 3 | `cli-anything-n8n config set ...` |

Extra: `N8N_TIMEOUT` env var (default: 30 seconds)

### n8n compatibility

| n8n Version | API Version | Status |
|-------------|-------------|--------|
| >= 1.0.0 | v1.1.1 | Verified |
| 2.43.0 | v1.1.1 | Tested (E2E) |

### Project structure

```
cli_anything/n8n/
├── n8n_cli.py          # CLI + interactive REPL
├── core/               # API wrappers (one file per resource)
│   ├── workflows.py    # 9 endpoints
│   ├── executions.py   # 4 endpoints
│   ├── credentials.py  # 4 endpoints
│   ├── variables.py    # 4 endpoints
│   ├── tags.py         # 5 endpoints
│   └── project.py      # Config management
├── utils/
│   ├── n8n_backend.py  # HTTP client (X-N8N-API-KEY auth)
│   └── repl_skin.py    # Terminal UI (colors, tables)
└── tests/
    ├── test_core.py    # 33 unit tests (mocked)
    └── test_full_e2e.py # 11 E2E tests (live n8n)
```

### Development

```bash
git clone https://github.com/webcomunicasolutions/cli-n8n.git
cd cli-n8n
pip install -e .
pip install pytest

# Unit tests (no n8n needed)
pytest cli_anything/n8n/tests/test_core.py -v

# E2E tests (needs running n8n)
export N8N_BASE_URL=https://your-n8n.com
export N8N_API_KEY=your-key
pytest cli_anything/n8n/tests/test_full_e2e.py -v
```

### License

MIT - [Juan Jose Sanchez Bernal](mailto:info@webcomunica.solutions) / [Webcomunica Soluciones Informaticas](https://webcomunica.solutions)

---

<a id="español"></a>

## Español

### Por que existe este proyecto

Si usas **[Claude Code](https://claude.ai/code)** (o cualquier agente IA de programacion) y quieres gestionar tus workflows de **[n8n](https://n8n.io)**, normalmente necesitas un **servidor MCP** — una integracion especial que conecta la IA con la API de n8n. Los MCP funcionan, pero tienen limitaciones:

- Consumen ventana de contexto (cada definicion de tool gasta tokens)
- Requieren configuracion especifica por IDE/cliente
- No son portables — no puedes usarlos fuera de Claude Code
- Añaden una capa de complejidad entre la IA y la API

**cli-anything-n8n** toma un enfoque diferente: es una **herramienta CLI estandar** que cualquier agente IA puede usar mediante comandos de shell normales. Sin MCP. Sin integracion especial. Solo `pip install` y a funcionar.

```
# Con MCP (setup complejo, especifico por IDE):
Claude Code -> Servidor MCP -> API n8n

# Con cli-anything-n8n (universal, sin configuracion):
Claude Code -> shell -> cli-anything-n8n -> API n8n
Cualquier agente IA -> shell -> cli-anything-n8n -> API n8n
Tu -> terminal -> cli-anything-n8n -> API n8n
```

### Como se construyo

Este proyecto se construyo enteramente con **Claude Code** en una sola sesion:

1. **Investigacion** — Analisis del framework [CLI-Anything](https://github.com/HKUDS/CLI-Anything) (25k+ stars) y la API REST de n8n
2. **Verificacion de API** — Descarga de la especificacion OpenAPI real de una instancia n8n 2.43.0 (`/api/v1/openapi.yml`) para verificar que endpoints existen realmente en la API publica
3. **Implementacion** — CLI completo siguiendo el patron CLI-Anything: comandos Click, cliente HTTP, modo REPL, salida coloreada
4. **Testing** — 44 tests automatizados (33 unitarios + 11 E2E contra n8n real)
5. **Publicacion** — Publicado en [PyPI](https://pypi.org/project/cli-anything-n8n/) y enviado [PR a CLI-Anything](https://github.com/HKUDS/CLI-Anything/pull/171)

Solo se exponen endpoints verificados y funcionales. Muchas funcionalidades de n8n (Data Tables, listar credenciales, parar ejecuciones) **no estan** en la API publica — no fingimos que funcionan.

### Pruebalo ahora (2 minutos)

```bash
# 1. Instalar
pip install cli-anything-n8n

# 2. Conectar a tu n8n
export N8N_BASE_URL=https://tu-instancia-n8n.com
export N8N_API_KEY=tu-api-key

# 3. Usar
cli-anything-n8n workflow list
cli-anything-n8n --json execution list --status error
cli-anything-n8n tag create "produccion"
```

> **Donde consigo mi API key?** En n8n, ve a Settings > API > Create API Key.

### Uso con Claude Code (o cualquier agente IA)

El flag `--json` hace la salida legible por maquinas. Cualquier agente IA que pueda ejecutar comandos de shell puede usarlo:

```bash
# Claude Code puede ejecutar esto directamente:
cli-anything-n8n --json workflow list
cli-anything-n8n --json workflow get ABC123
cli-anything-n8n --json execution list --status error --limit 5
cli-anything-n8n workflow create @workflow.json
```

Sin configuracion MCP. Sin definiciones de tools consumiendo tu ventana de contexto. Solo comandos de shell.

### Modo REPL interactivo

```bash
cli-anything-n8n
n8n> workflow list --active
n8n> execution list --status error
n8n> tag list
n8n> exit
```

### Todos los comandos

| Grupo | Comandos | Que hace |
|-------|----------|----------|
| **workflow** | list, get, create, update, delete, activate, deactivate, tags, set-tags, transfer | Gestionar workflows |
| **execution** | list, get, delete, retry | Revisar y reintentar ejecuciones |
| **credential** | create, delete, schema, transfer | Gestionar credenciales |
| **variable** | list, create, update, delete | Gestionar variables de entorno |
| **tag** | list, get, create, update, delete | Organizar con tags |
| **config** | show, set | Guardar configuracion de conexion |

### Exportar e importar workflows

Mueve workflows entre instancias o haz backups:

```bash
# Exportar un workflow a JSON
cli-anything-n8n workflow export ABC123

# Importar en otra instancia
cli-anything-n8n workflow import backup.json

# Importar con otro nombre
cli-anything-n8n workflow import backup.json --name "Copia de Mi Workflow"
```

### Dashboard de estado

Ver todo de un vistazo:

```bash
cli-anything-n8n status
```

### Monitoreo en tiempo real

```bash
# Ver ejecuciones en vivo (cada 5 segundos)
cli-anything-n8n execution watch

# Solo un workflow
cli-anything-n8n execution watch --workflow-id ABC123
```

### Guardar conexion

```bash
cli-anything-n8n config set base_url https://tu-instancia-n8n.com
cli-anything-n8n config set api_key tu-api-key

# Ahora usalo directamente
cli-anything-n8n workflow list
```

### Compatibilidad con n8n

| Version n8n | Version API | Estado |
|-------------|-------------|--------|
| >= 1.0.0 | v1.1.1 | Verificado |
| 2.43.0 | v1.1.1 | Testeado (E2E) |

### Desarrollo

```bash
git clone https://github.com/webcomunicasolutions/cli-n8n.git
cd cli-n8n
pip install -e .
pip install pytest
pytest cli_anything/n8n/tests/test_core.py -v
```

### Licencia

MIT - [Juan Jose Sanchez Bernal](mailto:info@webcomunica.solutions) / [Webcomunica Soluciones Informaticas](https://webcomunica.solutions)
