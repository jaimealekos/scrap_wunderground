# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-07-13

### Fixed

- `scrap_wunderground()` never returned the extracted rows (missing `return`).
- Undefined variable (`NameError`) when the HTTP request did not return 200;
  HTTP errors now raise `requests.HTTPError` via `raise_for_status()`.
- The function extracted every column of the table instead of only
  'Time', 'Precip. Rate' and 'Precip. Accum.' as documented. Columns are now
  selected by header name, tolerating minor variations such as
  'Precip. Rate.'.

### Added

- Command line interface: `python scrap_wunderground.py <station_table_url>`.
- Request timeout and browser-like `User-Agent` header.
- Module and function docstrings, `__version__` attribute.
- Project files: `README.md`, `LICENSE` (MIT), `requirements.txt`,
  `.gitignore` and this changelog.

## [1.0.0] - 2024-12-08

### Added

- Initial version: downloads a Weather Underground PWS daily table page and
  parses its observation rows with BeautifulSoup.

[1.0.1]: https://github.com/jaimealekos/scrap_wunderground/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/jaimealekos/scrap_wunderground/releases/tag/v1.0.0
