# Migration to uv + pyproject.toml

**Date**: 2026-02-04
**Status**: ✅ Completed

## What Changed

Migrated from pip-style `requirements.txt`/`requirements.in` files to modern `uv` + `pyproject.toml` dependency management.

## Old Approach (Deprecated)
```bash
# Old way - DO NOT USE
uv pip install -r core_requirements.txt
uv pip install -r dev_requirements.txt
```

## New Approach (Current)
```bash
# Production dependencies
uv sync

# With test dependencies
uv sync --group test

# With development dependencies
uv sync --group dev

# All groups
uv sync --all-groups
```

## Files Removed
- ❌ `core_requirements.in`
- ❌ `core_requirements.txt`
- ❌ `dev_requirements.in`

## Files Updated
- ✅ `pyproject.toml` - All dependencies now defined here
- ✅ `.github/workflows/test.yml` - CI uses `uv sync --group test`

## Platform-Specific Dependencies

The following dependencies are now properly marked with platform markers:

### Windows Only
- `pywin32>=311` (sys_platform == 'win32')
- `win32-setctime>=1.2.0` (sys_platform == 'win32')
- `hypercorn>=0.18.0` (sys_platform == 'win32')

### Unix Only
- `gunicorn>=25.0.1` (sys_platform != 'win32')

This fixes the CI installation failure where `pywin32` was being installed on Ubuntu runners.

## Benefits

1. **Single source of truth**: All dependencies in `pyproject.toml`
2. **Platform awareness**: Proper platform markers prevent installation failures
3. **Faster resolution**: `uv` lockfile (`uv.lock`) ensures reproducible installs
4. **Modern tooling**: Aligned with Python packaging standards (PEP 621)
5. **Dependency groups**: Separate dev/test dependencies cleanly

## For Developers

### First Time Setup
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone <repo>
cd strategiq
uv sync --all-groups
```

### Running Tests
```bash
uv run pytest
```

### Adding Dependencies
```bash
# Add to [project] dependencies in pyproject.toml
# Then sync
uv sync
```

## CI/CD

GitHub Actions now uses:
```yaml
- name: Install dependencies
  run: uv sync --group test

- name: Run tests
  run: uv run pytest --cov=src
```

No more manual pip install steps!
