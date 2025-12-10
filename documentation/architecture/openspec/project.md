# Project Context

## Purpose
This project provides a falsey sentinel singleton and factory for representing absent values in contexts where `None` or `False` might be valid values. It offers a type-safe, immutable alternative to `None` for distinguishing between "empty" and "missing" states.

## Tech Stack
- **Language**: Python 3.10+
- **Build System**: Hatch
- **Linting & Formatting**: Ruff, isort, emcd-vibe-linter
- **Type Checking**: Pyright
- **Testing**: pytest, coverage
- **Documentation**: Sphinx
- **Release Management**: Towncrier

## Project Conventions

### Code Style
- **Formatting**: 4-space indentation, 79-character line length (enforced by Ruff/isort).
- **Import Style**: Centralized external imports in `__/imports.py` and package re-exports in `__/`. Modules import from `.` or `.__` (e.g., `from . import __`).
- **Linter Rules**: Strict adherence to Ruff rulesets as defined in `pyproject.toml`.
- **References**:
  - `documentation/architecture/filesystem.rst` (Source Code Organization, Component Integration)

### Architecture Patterns
- **Module Structure**: Flat module structure (`objects`, `installers`, `exceptions`, `__`) to maintain simplicity and avoid circular dependencies.
- **Patterns**:
  - **Singleton Pattern**: Used for the global `absent` sentinel.
  - **Factory Pattern**: `AbsenceFactory` for creating custom sentinels.
  - **Inheritance**: Inherits falsey behavior from `falsifier.Falsifier`.
- **References**:
  - `documentation/architecture/summary.rst` (System Overview, Key Architectural Patterns)
  - `documentation/architecture/filesystem.rst` (Dependency Graph)

### Testing Strategy
- **Framework**: `pytest` with `coverage`.
- **Structure**: Tests mirror source structure in `tests/` directory.
- **Naming**: Test files `test_*.py`. Test functions use numbered prefixes (e.g., `test_100_exceptions`, `test_201_absent_singleton_identity`) for systematic coverage.
- **References**:
  - `documentation/architecture/filesystem.rst` (Testing Integration)

### Git Workflow
- **Updates**: Project structure updated via Copier.

## Domain Context
- **Absence vs None**: The core domain concept is the distinction between `None` (a specific value often meaning "null") and `absent` (meaning "no value provided").
- **Falsiness**: The sentinel is "falsey" (evaluates to False in boolean contexts) to play nicely with Python control flow, but unique to allow distinguishing from other falsey values (0, False, empty list).

## Important Constraints
- **Minimal Dependencies**: Keep dependency footprint small (`classcore`, `dynadoc`, `falsifier`, `typing-extensions`).
- **Pickling**: The `absent` sentinel and factory instances do not support pickling.
- **Backward Compatibility**: Public API at `absence.*` must remain stable.

## External Dependencies
- `classcore`: Attribute visibility and object utilities.
- `dynadoc`: Documentation tools.
- `falsifier`: Base class for falsey objects.
- `typing-extensions`: Type hinting support.
