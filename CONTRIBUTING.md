# Contributing to pse-python-sdk

## Getting Started

1. **Fork & clone** the repository:

   ```bash
   git clone https://github.com/FranekGit/pse-python-sdk.git
   cd pse-python-sdk
   ```

2. **Install [uv](https://docs.astral.sh/uv/getting-started/installation/)** and sync the environment (creates `.venv` with the package and dev dependencies, pinned by `uv.lock`):

   ```bash
   uv sync
   ```

3. **Checkout `develop`** — all feature work starts here:

   ```bash
   git checkout develop
   ```

## Branching Strategy

The two long-lived branches:

| Branch | Purpose |
|--------|---------|
| `main` | Stable, production-ready releases |
| `develop` | Integration branch for the next release |

Short-lived branches for specific work:

| Branch | From | Merges back to | Purpose |
|--------|------|----------------|---------|
| `feature/<name>` | `develop` | `develop` | New features |
| `bugfix/<name>` | `develop` | `develop` | Non-critical bug fixes |
| `release/<version>` | `develop` | `main` + `develop` | Release preparation |
| `hotfix/<name>` | `main` | `main` + `develop` | Critical production fixes |

## Development Workflow

Run these from the project root:

```bash
# Run tests
uv run pytest

# Lint
uv run ruff check src/ scripts/ tests/

# Format
uv run ruff format src/ scripts/ tests/
```

Fix any lint/test failures before opening a PR.

## Endpoint Registry

`src/pse_sdk/_registry.py` is generated from the PSE OpenAPI spec (`https://api.raporty.pse.pl/api/openapi`) — don't edit it by hand.

```bash
# Regenerate from the live spec
uv run scripts/gen_registry.py

# Check that the committed registry is up to date
uv run scripts/gen_registry.py --check
```

## Endpoint Docs

`docs/endpoints.md` is generated from the registry — don't edit it by hand. Regenerate it after any registry change.

```bash
# Regenerate
uv run scripts/gen_docs.py

# Check that the committed docs are up to date
uv run scripts/gen_docs.py --check
```

## Dependencies

Dev dependencies live in the `dev` dependency group in `pyproject.toml`; exact versions are pinned in `uv.lock`.

```bash
# Add a dev dependency
uv add --dev <package>

# Upgrade a single locked package
uv lock --upgrade-package <package>
```

Commit `uv.lock` together with any `pyproject.toml` dependency change.

## Commit Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <short description>
```

Supported types:

| Type | Use for |
|------|---------|
| `feat:` | New features |
| `fix:` | Bug fixes |
| `refactor:` | Code restructuring (no behavior change) |
| `test:` | Adding or updating tests |
| `docs:` | Documentation changes |
| `chore:` | Maintenance tasks (deps, CI, config) |


## Pull Requests

- **Target `develop`** for `feature/*` and `bugfix/*` branches.
- **Target `main`** only for `hotfix/*` and `release/*` branches.
- Ensure tests pass and linting is clean before requesting review.
