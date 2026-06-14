import unicodedata
from typing import Union

from num2words import num2words

from alphabetic_sort.exceptions import NumberConversionError, UnsupportedLanguageError
from alphabetic_sort.locale_map import SUPPORTED_LOCALES, resolve_locale

Number = Union[int, float]


def number_to_word(number: Number, locale: str) -> str:
    """Convert a single number to its word. Locale must already be resolved."""
    try:
        return num2words(number, lang=locale)
    except Exception as exc:
        raise NumberConversionError(
            f"Cannot convert {number!r} with locale {locale!r}: {exc}"
        ) from exc


def _sort_key(word: str, locale_aware: bool) -> str:
    if locale_aware:
        return unicodedata.normalize("NFKD", word.casefold())
    return word


def alphabetic_sort(
    numbers: list[Number],
    lang: str,
    *,
    locale_aware: bool = False,
    return_words: bool = False,
) -> "list[Number] | tuple[list[Number], list[str], list[str]]":
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
            raise TypeError(
                f"All elements must be int or float, got {type(n).__name__}: {n!r}"
            )

    if not numbers:
        if return_words:
            return [], [], []
        return []

    locale = resolve_locale(lang)

    # Words for each input number in original order (full representation for display)
    original_words = [number_to_word(n, locale) for n in numbers]

    # Partition into negatives (< 0) and non-negatives (>= 0)
    # For negatives, the sort key is the word for the absolute value
    negatives: list[tuple[Number, str]] = [
        (n, number_to_word(abs(n), locale)) for n in numbers if n < 0
    ]
    non_negatives: list[tuple[Number, str]] = [
        (n, number_to_word(n, locale)) for n in numbers if n >= 0
    ]

    # Negatives: reverse alphabetical by absolute value word
    sorted_neg = sorted(
        negatives, key=lambda p: _sort_key(p[1], locale_aware), reverse=True
    )
    # Non-negatives: normal alphabetical
    sorted_pos = sorted(
        non_negatives, key=lambda p: _sort_key(p[1], locale_aware)
    )

    sorted_numbers: list[Number] = (
        [p[0] for p in sorted_neg] + [p[0] for p in sorted_pos]
    )

    if return_words:
        sorted_words = [number_to_word(n, locale) for n in sorted_numbers]
        return sorted_numbers, original_words, sorted_words

    return sorted_numbers


def get_supported_languages() -> list[str]:
    """Return sorted list of all num2words locale keys supported by this library."""
    return list(SUPPORTED_LOCALES)
