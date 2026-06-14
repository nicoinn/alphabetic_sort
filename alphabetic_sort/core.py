from __future__ import annotations

import unicodedata
from typing import Literal, overload

from num2words import num2words

from alphabetic_sort.exceptions import NumberConversionError
from alphabetic_sort.locale_map import SUPPORTED_LOCALES, resolve_locale

Number = int | float


def number_to_word(number: Number, locale: str) -> str:
    """Convert a single number to its word. Locale must already be resolved."""
    try:
        return str(num2words(number, lang=locale))  # type: ignore[no-untyped-call]
    except Exception as exc:
        raise NumberConversionError(
            f"Cannot convert {number!r} with locale {locale!r}: {exc}"
        ) from exc


def _sort_key(word: str, locale_aware: bool) -> str:
    if locale_aware:
        return unicodedata.normalize("NFKD", word.casefold())
    return word


@overload
def alphabetic_sort(
    numbers: list[Number],
    lang: str,
    *,
    locale_aware: bool = ...,
    return_words: Literal[False] = ...,
) -> list[Number]: ...


@overload
def alphabetic_sort(
    numbers: list[Number],
    lang: str,
    *,
    locale_aware: bool = ...,
    return_words: Literal[True],
) -> tuple[list[Number], list[str], list[str]]: ...


def alphabetic_sort(
    numbers: list[Number],
    lang: str,
    *,
    locale_aware: bool = False,
    return_words: bool = False,
) -> list[Number] | tuple[list[Number], list[str], list[str]]:
    """
    Sort numbers by the alphabetical order of their word representations.

    Sorting rules:
    - Negative numbers always come before non-negatives (zero is non-negative).
    - Negatives are sorted among themselves in REVERSE alphabetical order of
      their absolute value word (the word "minus" is ignored for sorting).
    - Non-negatives are sorted in normal alphabetical order.
    - Both int and float are supported.

    Parameters
    ----------
    numbers : list of int or float
    lang : str
        BCP 47-style language tag (e.g. 'en_UK', 'fr_BE', 'de_DE').
        Normalized via resolve_locale().
    locale_aware : bool
        If True, use NFKD Unicode normalization for sort key (better for accented
        scripts). Default False.
    return_words : bool
        If True, return a 3-tuple: (sorted_numbers, original_words, sorted_words).
        original_words[i] is the word for numbers[i]; sorted_words[i] is the word
        for sorted_numbers[i]. Useful for showing intermediate steps.

    Raises
    ------
    UnsupportedLanguageError, NumberConversionError, TypeError
    """
    if not isinstance(numbers, list):
        raise TypeError(f"numbers must be a list, got {type(numbers).__name__}")
    for n in numbers:
        if not isinstance(n, (int, float)):
            raise TypeError(f"All elements must be int or float, got {type(n).__name__}: {n!r}")

    if not numbers:
        if return_words:
            return [], [], []
        return []

    locale = resolve_locale(lang)

    # Collect every unique value that needs converting:
    # - each number (for its display word)
    # - abs(n) for each negative (sort key ignores "minus"; may coincide with
    #   an existing positive in the list, in which case it's free)
    to_convert: set[Number] = set(numbers)
    to_convert.update(abs(n) for n in numbers if n < 0)  # type: ignore[arg-type]

    # One num2words call per unique value — eliminates the 2-3x redundant
    # conversions of the naive approach (positives went from 2-3 calls to 1).
    word_cache: dict[Number, str] = {n: number_to_word(n, locale) for n in to_convert}

    original_words = [word_cache[n] for n in numbers]

    negatives: list[tuple[Number, str]] = [
        (n, word_cache[abs(n)])
        for n in numbers
        if n < 0  # type: ignore[index]
    ]
    non_negatives: list[tuple[Number, str]] = [(n, word_cache[n]) for n in numbers if n >= 0]

    sorted_neg = sorted(negatives, key=lambda p: _sort_key(p[1], locale_aware), reverse=True)
    sorted_pos = sorted(non_negatives, key=lambda p: _sort_key(p[1], locale_aware))

    sorted_numbers: list[Number] = [p[0] for p in sorted_neg] + [p[0] for p in sorted_pos]

    if return_words:
        sorted_words = [word_cache[n] for n in sorted_numbers]
        return sorted_numbers, original_words, sorted_words

    return sorted_numbers


def get_supported_languages() -> list[str]:
    """Return sorted list of all num2words locale keys supported by this library."""
    return list(SUPPORTED_LOCALES)
