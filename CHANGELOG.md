# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- `OutputFormat` enum for controlling response format (JSON, CSV, XML)
- `HTTPClient` for managing HTTP requests with pagination support
- Coverage of the `price-cost` PSE API endpoint
- Date normalization and validation utilities
- Configurable `base_url` and `page_size` parameters
- Optional pandas integration via `pip install pse-sdk[pandas]`
- Unit tests for PSEClient and HTTPClient

### Documentation
- README with installation, usage examples, and endpoint reference
- CONTRIBUTING.md with branching strategy and development workflow
- Endpoint documentation
