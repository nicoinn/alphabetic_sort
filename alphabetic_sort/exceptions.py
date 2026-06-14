class AlphabeticSortError(Exception):
    """Base exception for the alphabetic_sort library."""


class UnsupportedLanguageError(AlphabeticSortError):
    """Raised when the given language code cannot be resolved to a num2words locale."""

    def __init__(self, lang: str) -> None:
        self.lang = lang
        super().__init__(f"Unsupported language code: {lang!r}")


class NumberConversionError(AlphabeticSortError):
    """Raised when a number cannot be converted to words."""
