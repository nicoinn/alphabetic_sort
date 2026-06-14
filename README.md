# alphabetic_sort

> Sort numbers by the alphabetical order of their name in any language.

## What is this?

Numbers, when written out as words, have a perfectly valid alphabetical order.
*Eight* comes before *five*, which comes before *four*, which comes before *nine*,
and so on. This order has nothing to do with numerical value — it is purely
determined by how the words are spelled. Most of the time this is completely
useless. Occasionally, it is exactly what you need.

Naturally, this is entirely language-dependent. In English, *eight* sorts first
among 1–9. In German it is *acht*, which also sorts first (German and English
agree on this one — enjoy it, it is rare). In French it is *deux*. Same numbers,
completely different order. The numbers do not care. They never did.

This library takes a list of numbers and sorts them the way a dictionary would:
by converting each number to its written word form in a given language, sorting
those words alphabetically, and returning the original numbers in that new order.

```python
from alphabetic_sort import alphabetic_sort

alphabetic_sort([1, 5, 12], lang="en_UK")
# → [5, 1, 12]
# because "five" < "one" < "twelve"
```

The result looks wrong at first glance. That is the point.

## Origin

The idea came from a real-world encounter. A biologist colleague once sent over
an Excel sheet containing a long list of sample numbers. They had sorted the
column themselves — and because Excel, left to its own devices, had treated the
values as text, the numbers ended up in alphabetical order: 1, 10, 100, 11, 12,
2, 20, 21... The biologist saw nothing wrong with this. The data was sorted, after
all. Alphabetically sorted numbers are a thing that exists in the wild.

That conversation stuck. This library is the result.

## A note on how this was built

This entire project — library, tests, CI pipeline, web UI, and documentation —
was written by [Claude](https://claude.ai) on a Sunday, entirely from a cell phone,
while going about a perfectly ordinary day. No laptop, no desk, no dedicated coding
session. Just a series of prompts tapped out between whatever else the day had going
on. The code is real, the tests pass, and the whole thing is published to GitHub.

Make of that what you will.

---

Yes, this is a joke. It works for real.

```python
from alphabetic_sort import alphabetic_sort

alphabetic_sort([1, 5, 12], lang="en_UK")
# → [5, 1, 12]
# because "five" < "one" < "twelve"
```

## Installation

```bash
pip install alphabetic_sort
```

Requires Python 3.11+.

## Usage

```python
from alphabetic_sort import alphabetic_sort

# Integers
alphabetic_sort([1, 5, 12], lang="en")       # → [5, 1, 12]

# Floats
alphabetic_sort([1.5, 0.5, 2.5], lang="en")  # → [1.5, 2.5, 0.5]
                                              # "one.." < "two.." < "zero.."

# French Belgian (septante/nonante, not soixante-dix/quatre-vingt-dix)
alphabetic_sort([11, 90], lang="fr_BE")       # → [90, 11]
# "nonante" < "onze"  (n < o)

alphabetic_sort([11, 90], lang="fr")          # → [11, 90]
# "onze" < "quatre-vingt-dix"  (o < q)

# German
alphabetic_sort(list(range(1, 13)), lang="de")
# → [8, 3, 1, 11, 5, 9, 6, 7, 4, 10, 2, 12]
# acht, drei, eins, elf, fünf, neun, sechs, sieben, vier, zehn, zwei, zwölf
```

### Negative numbers

Negatives always sort before non-negatives. Among negatives, sorting is in
**reverse** alphabetical order of the absolute value word ("minus" is ignored).

```python
alphabetic_sort([-5, -1, -12, 3, 7], lang="en")
# → [-12, -1, -5, 7, 3]
#
# Negatives (rev alpha of abs): twelve > one > five  →  -12, -1, -5
# Positives (alpha):            seven < three        →   7, 3
```

Zero is treated as non-negative.

### Intermediate steps

Pass `return_words=True` to get the words used at each stage:

```python
sorted_nums, original_words, sorted_words = alphabetic_sort(
    [1, 5, 12], lang="en", return_words=True
)
# sorted_nums    → [5, 1, 12]
# original_words → ["one", "five", "twelve"]  (matches input order)
# sorted_words   → ["five", "one", "twelve"]  (matches output order)
```

### Language codes

Pass any BCP 47 language tag — it is normalized automatically:

```python
alphabetic_sort([1, 5, 12], lang="en_UK")   # same as "en"
alphabetic_sort([1, 5, 12], lang="en-GB")   # same as "en"
alphabetic_sort([1, 5, 12], lang="fr_BE")   # Belgian French (septante/nonante)
alphabetic_sort([1, 5, 12], lang="de_AT")   # same as "de"
```

Regional variants with genuinely distinct words are preserved:

| Variant | Distinct words |
|---------|---------------|
| `fr_BE` | septante (70), nonante (90) |
| `fr_CH` | septante (70), huitante (80), nonante (90) |
| `pt_BR` | Brazilian Portuguese |
| `en_IN` | Indian English |

### Supported languages

56 locales via [num2words](https://github.com/savoirfairelinux/num2words):

`am ar az be bn ca ce cs cy da de en en_IN en_NG eo es es_CO es_CR es_GT es_NI es_VE fa fi fr fr_BE fr_CH fr_DZ he hu id is it ja kn ko kz lt lv nl no pl pt pt_BR ro ru sk sl sr sv te tet tg th tr uk vi`

```python
from alphabetic_sort import get_supported_languages
get_supported_languages()  # → sorted list of all 56 locale keys
```

## Performance and multithreading

The number-to-word conversion step (`num2words`) dominates runtime for large
inputs. The library eliminates redundant calls by building a word cache before
sorting: each unique number (and the absolute value of each negative) is
converted exactly once.

The `workers` parameter exposes an optional `ThreadPoolExecutor` for that
conversion step. The default is `workers=1` (single-threaded).

**On standard Python builds (GIL enabled — 3.11, 3.12, 3.13):** threading
adds overhead rather than removing it. The GIL serializes the num2words calls
regardless of how many threads you spawn, while thread management still costs
time. Leave `workers=1` on these builds.

**On free-threaded Python builds (3.13t, 3.14t+):** the GIL is disabled and
threads genuinely run in parallel. `workers=4` (or higher) gives near-linear
speedup on large inputs. This is the intended use case for the parameter.

```python
# Free-threaded Python only — no benefit on standard builds
alphabetic_sort(large_list, lang="en", workers=4)
```

The CI benchmark workflow (`benchmark.yml`) measures this automatically across
Python 3.11–3.15 with and without free-threading, and publishes results to the
GitHub Actions step summary so the numbers are always up to date.

## API

### `alphabetic_sort(numbers, lang, *, locale_aware=False, return_words=False, workers=1)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `numbers` | `list[int \| float]` | Numbers to sort |
| `lang` | `str` | BCP 47 language tag |
| `locale_aware` | `bool` | Use NFKD normalization for accented scripts |
| `return_words` | `bool` | Return `(sorted_numbers, original_words, sorted_words)` |
| `workers` | `int` | Thread-pool size for number→word conversion. Default `1`. Increase only on free-threaded Python (3.13t+). |

**Raises:** `UnsupportedLanguageError`, `NumberConversionError`, `TypeError`

### `get_supported_languages() → list[str]`

Returns a sorted list of all supported locale keys.

## Web UI

A demo web app is included in `webui/`:

```bash
pip install -r webui/requirements.txt
uvicorn webui.app:app --reload
# → http://127.0.0.1:8000
```

## License

Apache 2.0 — see [LICENSE](LICENSE).
