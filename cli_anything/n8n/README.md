# cli-anything-n8n

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![CLI-Anything](https://img.shields.io/badge/CLI--Anything-harness-orange.svg)](https://github.com/HKUDS/CLI-Anything)
[![n8n API v1.1.1](https://img.shields.io/badge/n8n-API%20v1.1.1-EA4B71.svg)](https://docs.n8n.io/api/api-reference/)
[![n8n >= 1.0.0](https://img.shields.io/badge/n8n-%3E%3D%201.0.0-EA4B71.svg)]()
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

> [Leer en Español](#spanish) | [Read in English](#english)

---

<a id="english"></a>

## English

CLI harness for [n8n](https://n8n.io) workflow automation — built with the [CLI-Anything](https://github.com/HKUDS/CLI-Anything) pattern.

Created as a **community contribution** to bring n8n into the CLI-Anything ecosystem. Verified against the **n8n OpenAPI spec v1.1.1** (n8n 2.43.0) — only endpoints that actually exist in the public API are exposed.

### Features

- **Verified n8n Public API coverage**: workflows, executions, credentials, variables, tags
- **Interactive REPL mode** with colored output, truncation indicators, and table formatting
- **JSON output** for AI agent consumption (`--json`)
- **Config persistence** at `~/.cli-anything/n8n/config.json`
- **Robust error handling**: clean messages for HTTP errors, connection failures, invalid JSON
- **PEP 420 namespace packaging** — coexists with other CLI-Anything harnesses

### Quick Start

```bash
pip install cli-anything-n8n

# Configure
export N8N_BASE_URL=https://your-n8n.example.com
export N8N_API_KEY=your-api-key

# Use
cli-anything-n8n workflow list
cli-anything-n8n --json execution list --status error
cli-anything-n8n tag create "production"
```

Or use the interactive REPL:

```bash
cli-anything-n8n
n8n> workflow list --active
n8n> execution list --status error
n8n> exit
```

### Command Groups

| Group | Commands | API Endpoints |
|-------|----------|---------------|
| `workflow` | list, get, create, update, delete, activate, deactivate, tags, set-tags, transfer | 9 |
| `execution` | list, get, delete, retry | 4 |
| `credential` | create, delete, schema, transfer | 4 |
| `variable` | list, create, update, delete | 4 |
| `tag` | list, get, create, update, delete | 5 |
| `config` | show, set | - |

> **Note**: Some n8n features (Data Tables, credential listing, execution stop) are not available through the public API. This CLI only exposes verified, working endpoints.

### Configuration

Three ways to configure (in priority order):

1. **CLI flags**: `--url` and `--api-key`
2. **Environment variables**: `N8N_BASE_URL`, `N8N_API_KEY`, `N8N_TIMEOUT`
3. **Config file**: `cli-anything-n8n config set base_url https://...`

### For AI Agents

- Always use `--json` for structured, parseable output
- Use `@file.json` to pass complex JSON payloads
- Check return codes: 0 = success, non-zero = error
- Workflow and execution IDs are strings
- Set `N8N_TIMEOUT` env var for long-running operations (default: 30s)

### n8n Compatibility

| n8n Version | API Version | Status |
|-------------|-------------|--------|
| >= 1.0.0 | v1.1.1 | Verified |
| 2.43.0 | v1.1.1 | Tested (E2E) |

### Development

```bash
git clone https://github.com/webcomunicasolutions/cli-n8n.git
cd cli-n8n
pip install -e .
pytest cli_anything/n8n/tests/test_core.py -v        # unit tests (no n8n needed)
pytest cli_anything/n8n/tests/test_full_e2e.py -v     # E2E (requires running n8n)
```

### Architecture

```
cli_anything/n8n/
├── n8n_cli.py              # Click CLI + REPL
├── core/                   # Business logic (thin API wrappers)
│   ├── workflows.py        # Workflow CRUD, activate/deactivate, tags, transfer
│   ├── executions.py       # Execution list, get, delete, retry
│   ├── credentials.py      # Credential create, delete, schema, transfer
│   ├── variables.py        # Variable CRUD
│   ├── tags.py             # Tag CRUD
│   └── project.py          # Config load/save
├── utils/
│   ├── n8n_backend.py      # HTTP client (sole point of contact with n8n API)
│   └── repl_skin.py        # Terminal UI (banner, colors, tables)
├── skills/
│   └── SKILL.md            # AI agent discovery document
└── tests/
    ├── test_core.py        # Unit tests (mocked)
    └── test_full_e2e.py    # E2E lifecycle tests
```

### License

MIT

---

<a id="spanish"></a>

## Español

CLI harness para [n8n](https://n8n.io) (automatizacion de workflows) — construido con el patron [CLI-Anything](https://github.com/HKUDS/CLI-Anything).

Creado como **contribucion a la comunidad** para integrar n8n en el ecosistema CLI-Anything. Verificado contra la **especificacion OpenAPI v1.1.1 de n8n** (n8n 2.43.0) — solo se exponen endpoints que realmente existen en la API publica.

### Caracteristicas

- **Cobertura verificada de la API publica de n8n**: workflows, ejecuciones, credenciales, variables, tags
- **Modo REPL interactivo** con salida coloreada, indicadores de truncado y tablas
- **Salida JSON** para consumo por agentes IA (`--json`)
- **Configuracion persistente** en `~/.cli-anything/n8n/config.json`
- **Manejo robusto de errores**: mensajes claros para errores HTTP, fallos de conexion, JSON invalido
- **PEP 420 namespace packaging** — coexiste con otros harnesses de CLI-Anything

### Inicio rapido

```bash
pip install cli-anything-n8n

# Configurar
export N8N_BASE_URL=https://tu-instancia-n8n.example.com
export N8N_API_KEY=tu-api-key

# Usar
cli-anything-n8n workflow list
cli-anything-n8n --json execution list --status error
cli-anything-n8n tag create "produccion"
```

### Grupos de comandos

| Grupo | Comandos | Endpoints API |
|-------|----------|---------------|
| `workflow` | list, get, create, update, delete, activate, deactivate, tags, set-tags, transfer | 9 |
| `execution` | list, get, delete, retry | 4 |
| `credential` | create, delete, schema, transfer | 4 |
| `variable` | list, create, update, delete | 4 |
| `tag` | list, get, create, update, delete | 5 |
| `config` | show, set | - |

> **Nota**: Algunas funcionalidades de n8n (Data Tables, listar credenciales, parar ejecuciones) no estan disponibles via la API publica. Este CLI solo expone endpoints verificados y funcionales.

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
pytest cli_anything/n8n/tests/test_core.py -v        # tests unitarios
pytest cli_anything/n8n/tests/test_full_e2e.py -v     # E2E (requiere n8n corriendo)
```

### Licencia

MIT
