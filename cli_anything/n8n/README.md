# cli-anything-n8n

> [Leer en Español](#spanish) | [Read in English](#english)

---

<a id="english"></a>

## English

CLI harness for [n8n](https://n8n.io) workflow automation — built with the [CLI-Anything](https://github.com/HKUDS/CLI-Anything) pattern.

This project was created as a **community contribution** to bring n8n into the CLI-Anything ecosystem, making it controllable by AI agents and terminal power users alike.

### Features

- **Full n8n REST API coverage**: workflows, executions, credentials, variables, tags, data tables (44+ endpoints)
- **Interactive REPL mode** with colored output and table formatting
- **JSON output** for AI agent consumption (`--json`)
- **Config persistence** at `~/.cli-anything/n8n/config.json`
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
cli-anything-n8n variable create MY_VAR "my value"
```

Or use the interactive REPL:

```bash
cli-anything-n8n
n8n> workflow list
n8n> execution list --status error
n8n> exit
```

### Command Groups

| Group | Commands | Endpoints |
|-------|----------|-----------|
| `workflow` | list, get, create, update, delete, activate, deactivate, tags | 11 |
| `execution` | list, get, delete, retry, stop | 8 |
| `credential` | list, create, update, delete, schema | 6 |
| `variable` | list, create, update, delete | 4 |
| `tag` | list, get, create, update, delete | 5 |
| `table` | list, get, create, delete, rows, insert, update-rows | 10 |
| `config` | show, set | - |

### Configuration

Three ways to configure (in priority order):

1. **CLI flags**: `--url` and `--api-key`
2. **Environment variables**: `N8N_BASE_URL` and `N8N_API_KEY`
3. **Config file**: `cli-anything-n8n config set base_url https://...`

### For AI Agents

- Always use `--json` for structured, parseable output
- Use `@file.json` to pass complex JSON payloads: `cli-anything-n8n workflow create @my-workflow.json`
- Check return codes: 0 = success, non-zero = error
- Workflow and execution IDs are strings

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
│   ├── workflows.py        # Workflow CRUD, activate/deactivate
│   ├── executions.py       # Execution management
│   ├── credentials.py      # Credential CRUD + schema
│   ├── variables.py        # Variable CRUD
│   ├── tags.py             # Tag CRUD
│   ├── tables.py           # Data Table + Row CRUD
│   ├── project.py          # Config load/save
│   └── session.py          # REPL state
├── utils/
│   ├── n8n_backend.py      # HTTP client (single point of contact with n8n API)
│   └── repl_skin.py        # Terminal UI (banner, colors, tables)
├── skills/
│   └── SKILL.md            # AI agent discovery document
└── tests/
    ├── test_core.py        # 29 unit tests (mocked)
    └── test_full_e2e.py    # E2E lifecycle tests
```

### License

MIT

---

<a id="spanish"></a>

## Español

CLI harness para [n8n](https://n8n.io) (automatizacion de workflows) — construido con el patron [CLI-Anything](https://github.com/HKUDS/CLI-Anything).

Este proyecto fue creado como **contribucion a la comunidad** para integrar n8n en el ecosistema CLI-Anything, haciendolo controlable por agentes IA y usuarios avanzados de terminal.

### Caracteristicas

- **Cobertura completa de la API REST de n8n**: workflows, ejecuciones, credenciales, variables, tags, data tables (44+ endpoints)
- **Modo REPL interactivo** con salida coloreada y tablas formateadas
- **Salida JSON** para consumo por agentes IA (`--json`)
- **Configuracion persistente** en `~/.cli-anything/n8n/config.json`
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
cli-anything-n8n variable create MI_VAR "mi valor"
```

O usa el REPL interactivo:

```bash
cli-anything-n8n
n8n> workflow list
n8n> execution list --status error
n8n> exit
```

### Grupos de comandos

| Grupo | Comandos | Endpoints |
|-------|----------|-----------|
| `workflow` | list, get, create, update, delete, activate, deactivate, tags | 11 |
| `execution` | list, get, delete, retry, stop | 8 |
| `credential` | list, create, update, delete, schema | 6 |
| `variable` | list, create, update, delete | 4 |
| `tag` | list, get, create, update, delete | 5 |
| `table` | list, get, create, delete, rows, insert, update-rows | 10 |
| `config` | show, set | - |

### Configuracion

Tres formas de configurar (por orden de prioridad):

1. **Flags del CLI**: `--url` y `--api-key`
2. **Variables de entorno**: `N8N_BASE_URL` y `N8N_API_KEY`
3. **Archivo de config**: `cli-anything-n8n config set base_url https://...`

### Para agentes IA

- Usar siempre `--json` para salida estructurada y parseable
- Usar `@archivo.json` para payloads complejos: `cli-anything-n8n workflow create @mi-workflow.json`
- Verificar codigos de retorno: 0 = exito, distinto de 0 = error
- Los IDs de workflows y ejecuciones son strings

### Desarrollo

```bash
git clone https://github.com/webcomunicasolutions/cli-n8n.git
cd cli-n8n
pip install -e .
pytest cli_anything/n8n/tests/test_core.py -v        # tests unitarios (sin n8n)
pytest cli_anything/n8n/tests/test_full_e2e.py -v     # E2E (requiere n8n corriendo)
```

### Arquitectura

```
cli_anything/n8n/
├── n8n_cli.py              # CLI Click + REPL
├── core/                   # Logica de negocio (wrappers sobre la API)
│   ├── workflows.py        # CRUD workflows, activar/desactivar
│   ├── executions.py       # Gestion de ejecuciones
│   ├── credentials.py      # CRUD credenciales + schema
│   ├── variables.py        # CRUD variables
│   ├── tags.py             # CRUD tags
│   ├── tables.py           # CRUD Data Tables + filas
│   ├── project.py          # Carga/guardado de config
│   └── session.py          # Estado del REPL
├── utils/
│   ├── n8n_backend.py      # Cliente HTTP (unico punto de contacto con la API n8n)
│   └── repl_skin.py        # UI de terminal (banner, colores, tablas)
├── skills/
│   └── SKILL.md            # Documento de descubrimiento para agentes IA
└── tests/
    ├── test_core.py        # 29 tests unitarios (mockeados)
    └── test_full_e2e.py    # Tests E2E de ciclo de vida
```

### Licencia

MIT
