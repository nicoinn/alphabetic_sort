# alphabetic_sort

A Python library that sorts numbers by the alphabetical order of their word
representations in a given language. Yes, this is silly. It works for real.

## Project Structure

```
alphabetic_sort/       # The installable library package
├── __init__.py        # Public API exports + version
├── core.py            # alphabetic_sort(), get_supported_languages()
├── locale_map.py      # BCP 47 → num2words locale resolution
└── exceptions.py      # AlphabeticSortError, UnsupportedLanguageError, NumberConversionError

tests/
├── test_core.py       # Sort behavior, edge cases, regional variants
└── test_locale_map.py # Locale resolution (BCP 47, aliases, case, errors)

webui/                 # FastAPI demo (separate from library)
├── app.py             # FastAPI application
├── requirements.txt   # fastapi[standard], jinja2
└── templates/
    └── index.html     # 4-step Jinja2 template (no JS, no CDN)

pyproject.toml         # Build config and project metadata
requirements-dev.txt   # pytest, pytest-cov, httpx
```

## Installation

```bash
# From the repo root — installs the library + dev tools
pip install -e ".[dev]"

# WebUI dependencies
pip install -r webui/requirements.txt
```

## Running Tests

```bash
pytest                                          # all tests
pytest -v                                       # verbose
pytest --cov=alphabetic_sort --cov-report=term-missing   # with coverage
pytest tests/test_core.py -v -k "fr_BE"        # specific tests
```

All 54 tests pass.

## Running the WebUI

```bash
pip install -r webui/requirements.txt
uvicorn webui.app:app --reload
# Open http://127.0.0.1:8000
```

## API Reference

```python
from alphabetic_sort import alphabetic_sort, get_supported_languages
from alphabetic_sort.exceptions import UnsupportedLanguageError

# Basic usage
alphabetic_sort([1, 5, 12], lang="en_UK")        # → [5, 1, 12]

# Floats supported
alphabetic_sort([1.5, 0.5, 2.5], lang="en")      # → [1.5, 2.5, 0.5]

# Negative rules: negatives first, reverse-alpha of abs value (ignoring "minus")
alphabetic_sort([-5, -1, -12, 3, 7], lang="en")  # → [-12, -1, -5, 7, 3]

# With intermediate steps for display
nums, orig_words, sorted_words = alphabetic_sort(
    [1, 5, 12], lang="fr_BE", return_words=True
)

# List supported locales
get_supported_languages()  # → ['am', 'ar', 'az', ...]
```

## Sorting Rules

1. **Negatives always come before non-negatives** (zero is non-negative)
2. **Negatives** sorted in **reverse** alphabetical order of their absolute value word
   — "minus" is ignored for sorting purposes
3. **Non-negatives** sorted in normal alphabetical order
4. Both `int` and `float` are supported

Example with `[-5, -1, -12, 3, 7]` in `en`:
- Negatives: five, one, twelve → reverse: twelve, one, five → `[-12, -1, -5]`
- Positives: three, seven → alpha: seven, three → `[7, 3]`
- Result: `[-12, -1, -5, 7, 3]`

## Locale Resolution

BCP 47 tags are normalized to num2words locale keys:

| Input          | Resolves to | Note                          |
|----------------|-------------|-------------------------------|
| `en_UK`        | `en`        | alias                         |
| `en-GB`        | `en`        | hyphen normalized + alias     |
| `fr_BE`        | `fr_BE`     | preserved — distinct words    |
| `fr_CH`        | `fr_CH`     | preserved — huitante for 80   |
| `fr_FR`        | `fr`        | alias                         |
| `de_AT`        | `de`        | alias (no regional de variant)|
| `pt_BR`        | `pt_BR`     | preserved — distinct words    |
| `FR_BE`        | `fr_BE`     | case-insensitive match        |
| `xx`           | raises      | UnsupportedLanguageError      |

## Supported Languages (56 num2words locales)

am, ar, az, be, bn, ca, ce, cs, cy, da, de, en, en_IN, en_NG, eo,
es, es_CO, es_CR, es_GT, es_NI, es_VE, fa, fi, fr, fr_BE, fr_CH, fr_DZ,
he, hu, id, is, it, ja, kn, ko, kz, lt, lv, nl, no, pl, pt, pt_BR,
ro, ru, sk, sl, sr, sv, te, tet, tg, th, tr, uk, vi

Regional variants with distinct words (e.g. fr_BE uses *septante/nonante*
instead of *soixante-dix/quatre-vingt-dix*) are fully preserved.

## Key Design Decisions

- **num2words** handles all number→word conversion. No custom word lists.
- **Locale resolution** priority: exact match → case-insensitive exact match →
  explicit aliases → language subtag only → error. Never silently falls back to English.
- **Stable sort**: equal words preserve original list order (Python's sort is stable).
- **locale_aware=True** flag: uses NFKD Unicode normalization for sort key,
  giving better results for accented scripts (umlauts, etc.) without external deps.
- **WebUI** is fully independent — a FastAPI app that imports the library after
  `pip install -e .`. No JS, no CDN dependencies.

## Status

- [x] Core library (`alphabetic_sort/`)
- [x] Test suite — 54 tests, all passing
- [x] FastAPI WebUI (`webui/`)
- [x] CLAUDE.md
- [x] README.md
