# Contributing to pse-python-sdk

## Getting Started

1. **Fork & clone** the repository:

   ```bash
   git clone https://github.com/FranekGit/pse-python-sdk.git
   cd pse-python-sdk
   ```

2. **Set up a virtual environment** and install dev dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
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

Run these from the project root with your venv activated:

```bash
# Run tests
pytest

# Lint
ruff check src/ scripts/

# Format
ruff format src/ scripts/
```

Fix any lint/test failures before opening a PR.

## Endpoint Registry

`src/pse_sdk/_registry.py` is generated from the PSE OpenAPI spec (`https://api.raporty.pse.pl/api/openapi`) — don't edit it by hand.

```bash
# Regenerate from the live spec
python scripts/gen_registry.py

# Check that the committed registry is up to date
python scripts/gen_registry.py --check
```

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
