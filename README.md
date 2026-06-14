# alphabetic_sort

> Sort numbers by the alphabetical order of their name in any language.

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

## API

### `alphabetic_sort(numbers, lang, *, locale_aware=False, return_words=False)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `numbers` | `list[int \| float]` | Numbers to sort |
| `lang` | `str` | BCP 47 language tag |
| `locale_aware` | `bool` | Use NFKD normalization for accented scripts |
| `return_words` | `bool` | Return `(sorted_numbers, original_words, sorted_words)` |

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
