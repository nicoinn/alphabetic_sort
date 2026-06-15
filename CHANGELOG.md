# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.0.2] — 2026-06-15

### Changed

- CI: bump `actions/checkout` v4 → v6
- CI: bump `actions/upload-artifact` v4 → v7
- CI: bump `actions/download-artifact` v4 → v8
- CI: bump `codecov/codecov-action` v4 → v7
- CI: bump `softprops/action-gh-release` v2 → v3
- Build: relax `setuptools` pin from `<69.3` to `<82.1`

### Fixed

- Release workflow: add `on: workflow_call` to `ci.yml` so it can be used as a reusable workflow from `release.yml`
- Release workflow: add `workflow_dispatch` trigger to allow manual releases when tag pushes are blocked by the environment

---

## [0.0.1] — 2026-06-14

Initial release.

### Added

- `alphabetic_sort(numbers, lang)` — sort numbers by the alphabetical order of their word representations
- Support for 56 locales via [num2words](https://github.com/savoirfairelinux/num2words)
- BCP 47 language tag normalization (`en-GB`, `fr_BE`, `de_AT`, etc.)
- Regional variant preservation: `fr_BE` (septante/nonante) and `fr_CH` (huitante) produce genuinely different sort orders from `fr`
- Negative number support: negatives always sort before non-negatives, in reverse alphabetical order of their absolute value word
- Float support alongside integers
- `return_words=True` parameter to expose intermediate word representations
- `workers` parameter for optional multithreading (beneficial on free-threaded Python 3.13t+)
- `get_supported_languages()` helper
- `locale_aware=True` flag for NFKD Unicode normalization
- FastAPI + Jinja2 web UI demo (`webui/`)
- Full pytest suite (54 tests, 94% coverage)
- CI pipeline: lint (ruff + mypy), test matrix (Python 3.11–3.13), build verification
- Release pipeline: OIDC trusted publishing to TestPyPI and PyPI, GitHub Release creation
- Benchmark CI job across Python 3.11–3.15 (standard + free-threaded builds)

[0.0.2]: https://github.com/nicoinn/alphabetic_sort/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/nicoinn/alphabetic_sort/releases/tag/v0.0.1
