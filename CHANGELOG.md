# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `PSEClient.endpoints()`: names of all endpoints
- `PSEClient.columns(endpoint)`: data columns of an endpoint, in API order
  (meta columns left out). Both read the bundled registry, no HTTP request.

### Changed
- `docs/endpoints.md` is generated from the endpoint registry
  (`scripts/gen_docs.py`) and lists the data columns of all 90 endpoints,
  including the previously missing `wmb` and `his-gen-pal-sire`. The
  Description column is dropped.
- `fetch()` column and date-filter notes moved from `docs/endpoints.md` to
  the README

### Removed
- **Breaking:** all 32 `get_*` methods of `PSEClient` (`get_cen`, `get_csdac`,
  `get_kb`, `get_sk_cost`, `get_demand`, ...) and the internal `make_endpoint`
  helper. Use `fetch()` with the endpoint and column instead:
  `get_cen(s, e)` → `fetch("price-cost", s, e, columns=["cen_cost"])`.
  `fetch()` also returns the `*_utc` meta columns.

## [1.5.1] - 2026-10-20

### Added
- `docs/pse-api-endpoints-map.pdf`: endpoints map from the PSE API website

### Changed
- `docs/endpoints.md`: endpoints table now includes a Description column

## [1.5.0] - 2026-07-02

### Added
- `his-wlk-cal` endpoints to PSEClient (`get_demand`, `get_swm_p`, `get_swm_np`,
  `get_jg`, `get_jgw1`, `get_jgw2`, `get_jgm1`, `get_jgm2`, `get_jgz1`, `get_jgz2`,
  `get_jgz3`, `get_jga`, `get_jgo`, `get_jnwrb`, `get_jgm`, `get_wi`, `get_pv`)

### Fixed
- HTTP 400 on all endpoints: PSE API rejects percent-encoded `$` in query
  parameter names; `HTTPClient.fetch` now builds the query string manually

## [1.4.0] - 2026-04-09

### Added
- `sk` endpoints (`get_sk_d1_fcst`, `get_sk_d_fcst`, `get_sk_cost`) to PSEClient

## [1.3.0] - 2026-04-01

### Added
- Automatic retry with exponential backoff for failed API requests
- Request chunking for long date-range queries

## [1.2.0] - 2026-04-01

### Added
- `kmb-kro-rozl` endpoints to PSEClient
- `krb-rozl` endpoints to PSEClient

### Changed
- Refactor test suite with mock client fixture

## [1.1.0] - 2026-04-01

### Added
- `get_csdac` endpoint for accessing CSDAC PLN data from the PSE API

## [1.0.2] - 2026-03-31

### Fixed
- Remove invalid license entry from pyproject.toml

## [1.0.1] - 2026-03-13

### Documentation
- Add LICENSE.md with copyright and usage terms
- Add logo image
- Enhance endpoints documentation with detailed coverage and status badges
- Update example code in README.md for clarity
- Add API page link to README.md

## [1.0.0] - 2026-03-13

### Added
- `PSEClient` class for interacting with the PSE public REST API
- `OutputFormat` type (`Literal["dict", "dataframe"]`) for controlling response
  format: list of dicts or pandas DataFrame
- `HTTPClient` for managing HTTP requests with pagination support
- Coverage of the `price-cost` PSE API endpoint
- Date normalization and validation utilities
- Configurable HTTP `timeout` parameter
- Optional pandas integration via `pip install pse-sdk[pandas]`
- Unit tests for PSEClient and HTTPClient

### Documentation
- README with installation, usage examples, and endpoint reference
- CONTRIBUTING.md with branching strategy and development workflow
- Endpoint documentation
