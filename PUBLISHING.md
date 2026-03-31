# Publishing Guide / Guia de Publicacion

> [English](#english) | [Español](#spanish)

---

<a id="english"></a>

## English

### What is PyPI?

[PyPI](https://pypi.org) (Python Package Index) is the official repository for Python packages. When someone runs `pip install cli-anything-n8n`, pip downloads the package from PyPI. It's like npm for Node.js or Maven for Java.

### How we published this package

#### 1. Package structure

The `pyproject.toml` file defines everything about the package:
- **Name**: `cli-anything-n8n` (what users type in `pip install`)
- **Version**: `1.1.0`
- **Entry point**: `cli-anything-n8n` command -> `cli_anything.n8n.n8n_cli:main`
- **Dependencies**: click, prompt-toolkit, requests (installed automatically)

#### 2. Build the package

```bash
# Install build tools
pip install build twine

# Build (creates dist/ folder with .whl and .tar.gz)
python3 -m build
```

This creates two files in `dist/`:
- `cli_anything_n8n-1.1.0-py3-none-any.whl` — wheel (fast install)
- `cli_anything_n8n-1.1.0.tar.gz` — source distribution (fallback)

#### 3. Upload to PyPI

```bash
# Check the package is valid
python3 -m twine check dist/*

# Upload (needs PyPI account + API token)
python3 -m twine upload dist/* -u __token__ -p pypi-YOUR_TOKEN
```

#### 4. How to publish a new version

1. Update version in `pyproject.toml` and `n8n_cli.py` (VERSION constant)
2. Update `CHANGELOG.md`
3. Rebuild: `rm -rf dist/ && python3 -m build`
4. Upload: `python3 -m twine upload dist/*`
5. Commit and push to GitHub

#### PyPI account

- Website: https://pypi.org
- Your username: `webcomunica`
- API tokens: https://pypi.org/manage/account/token/
- **Important**: Create project-scoped tokens (not account-wide) for security

#### Your package page

https://pypi.org/project/cli-anything-n8n/

---

<a id="spanish"></a>

## Español

### Que es PyPI?

[PyPI](https://pypi.org) (Python Package Index) es el repositorio oficial de paquetes Python. Cuando alguien ejecuta `pip install cli-anything-n8n`, pip descarga el paquete de PyPI. Es como npm para Node.js o Maven para Java.

### Como publicamos este paquete

#### 1. Estructura del paquete

El archivo `pyproject.toml` define todo sobre el paquete:
- **Nombre**: `cli-anything-n8n` (lo que escribe el usuario en `pip install`)
- **Version**: `1.1.0`
- **Entry point**: comando `cli-anything-n8n` -> `cli_anything.n8n.n8n_cli:main`
- **Dependencias**: click, prompt-toolkit, requests (se instalan automaticamente)

#### 2. Construir el paquete

```bash
# Instalar herramientas de build
pip install build twine

# Construir (crea carpeta dist/ con .whl y .tar.gz)
python3 -m build
```

Esto crea dos archivos en `dist/`:
- `cli_anything_n8n-1.1.0-py3-none-any.whl` — wheel (instalacion rapida)
- `cli_anything_n8n-1.1.0.tar.gz` — distribucion fuente (respaldo)

#### 3. Subir a PyPI

```bash
# Verificar que el paquete es valido
python3 -m twine check dist/*

# Subir (necesita cuenta PyPI + token API)
python3 -m twine upload dist/* -u __token__ -p pypi-TU_TOKEN
```

#### 4. Como publicar una nueva version

1. Actualizar version en `pyproject.toml` y en `n8n_cli.py` (constante VERSION)
2. Actualizar `CHANGELOG.md`
3. Reconstruir: `rm -rf dist/ && python3 -m build`
4. Subir: `python3 -m twine upload dist/*`
5. Commit y push a GitHub

#### Cuenta PyPI

- Web: https://pypi.org
- Tu usuario: `webcomunica`
- Tokens API: https://pypi.org/manage/account/token/
- **Importante**: Crear tokens con scope del proyecto (no de toda la cuenta) por seguridad

#### Pagina de tu paquete

https://pypi.org/project/cli-anything-n8n/
