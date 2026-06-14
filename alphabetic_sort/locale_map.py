from num2words import CONVERTER_CLASSES

from alphabetic_sort.exceptions import UnsupportedLanguageError

# Maps lowercased locale keys back to the canonical casing used by num2words.
# e.g. "fr_be" → "fr_BE", "pt_br" → "pt_BR"
_LOWER_TO_LOCALE: dict[str, str] = {k.lower(): k for k in CONVERTER_CLASSES}

# Explicit overrides for BCP 47 codes that don't map cleanly to num2words keys.
# Keys are lowercased and use underscore as separator.
# IMPORTANT: Regional variants with distinct num2words entries (fr_BE, fr_CH, fr_DZ,
# pt_BR, en_IN, en_NG, es_CO, es_CR, es_GT, es_NI, es_VE) are intentionally NOT
# aliased here — they are preserved exactly in resolution step 2.
_ALIASES: dict[str, str] = {
    # English — only en, en_IN, en_NG in num2words
    "en_uk": "en",
    "en_gb": "en",
    "en_us": "en",
    "en_au": "en",
    "en_ca": "en",
    "en_nz": "en",
    "en_za": "en",
    # German — only de in num2words
    "de_at": "de",
    "de_ch": "de",
    "de_li": "de",
    "de_lu": "de",
    # French — fr, fr_BE, fr_CH, fr_DZ in num2words; others fall back to fr
    "fr_fr": "fr",
    "fr_ca": "fr",
    "fr_lu": "fr",
    "fr_mc": "fr",
    # Portuguese — pt, pt_BR in num2words
    "pt_pt": "pt",
    "pt_ao": "pt",
    "pt_mz": "pt",
    # Spanish — es + 5 regional variants in num2words; others fall back to es
    "es_es": "es",
    "es_mx": "es",
    "es_ar": "es",
    "es_cl": "es",
    "es_pe": "es",
    "es_bo": "es",
    "es_ec": "es",
    "es_uy": "es",
    "es_py": "es",
    "es_hn": "es",
    "es_sv": "es",
    "es_do": "es",
    "es_pa": "es",
    "es_cu": "es",
    # Norwegian variants
    "nb": "no",
    "nb_no": "no",
    "nn": "no",
    "nn_no": "no",
    "no_no": "no",
}

# All locale keys supported by num2words (and therefore by this library)
SUPPORTED_LOCALES: list[str] = sorted(CONVERTER_CLASSES.keys())


def resolve_locale(lang: str) -> str:
    """
    Normalize a BCP 47 language tag to a num2words locale key.

    Resolution order:
      1. Normalize separator: replace '-' with '_'
      2. Exact match against CONVERTER_CLASSES (preserves fr_BE, pt_BR, es_CO, etc.)
      3. Lowercase match
      4. Check _ALIASES (explicit overrides, lowercased key)
      5. Language subtag only (first segment, lowercased)
      6. Raise UnsupportedLanguageError
    """
    if not isinstance(lang, str):
        raise UnsupportedLanguageError(str(lang))

    normalized = lang.replace("-", "_")

    # Step 2: exact match (num2words keys are case-sensitive)
    if normalized in CONVERTER_CLASSES:
        return normalized

    # Step 3: case-insensitive exact match (preserves fr_BE, pt_BR casing)
    lower = normalized.lower()
    if lower in _LOWER_TO_LOCALE:
        return _LOWER_TO_LOCALE[lower]

    # Step 4: explicit aliases (keyed by lowercase)
    if lower in _ALIASES:
        return _ALIASES[lower]

    # Step 5: language subtag only
    base = lower.split("_")[0]
    if base in CONVERTER_CLASSES:
        return base

    raise UnsupportedLanguageError(lang)
