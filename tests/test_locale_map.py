import pytest

from alphabetic_sort.exceptions import UnsupportedLanguageError
from alphabetic_sort.locale_map import resolve_locale, SUPPORTED_LOCALES


def test_exact_match_base_locale():
    assert resolve_locale("en") == "en"
    assert resolve_locale("fr") == "fr"
    assert resolve_locale("de") == "de"
    assert resolve_locale("es") == "es"
    assert resolve_locale("it") == "it"
    assert resolve_locale("ru") == "ru"


def test_exact_match_regional_variants():
    # These must resolve to themselves, NOT fall back to the base language
    assert resolve_locale("fr_BE") == "fr_BE"
    assert resolve_locale("fr_CH") == "fr_CH"
    assert resolve_locale("fr_DZ") == "fr_DZ"
    assert resolve_locale("pt_BR") == "pt_BR"
    assert resolve_locale("en_IN") == "en_IN"
    assert resolve_locale("en_NG") == "en_NG"
    assert resolve_locale("es_CO") == "es_CO"
    assert resolve_locale("es_CR") == "es_CR"
    assert resolve_locale("es_GT") == "es_GT"
    assert resolve_locale("es_NI") == "es_NI"
    assert resolve_locale("es_VE") == "es_VE"


def test_hyphen_separator_normalized():
    assert resolve_locale("fr-BE") == "fr_BE"
    assert resolve_locale("pt-BR") == "pt_BR"
    assert resolve_locale("en-IN") == "en_IN"
    assert resolve_locale("de-DE") == "de"


def test_bcp47_aliases_en():
    assert resolve_locale("en_UK") == "en"
    assert resolve_locale("en_GB") == "en"
    assert resolve_locale("en_US") == "en"
    assert resolve_locale("en_AU") == "en"
    assert resolve_locale("en-US") == "en"


def test_bcp47_aliases_de():
    assert resolve_locale("de_AT") == "de"
    assert resolve_locale("de_CH") == "de"


def test_bcp47_aliases_fr():
    assert resolve_locale("fr_FR") == "fr"
    assert resolve_locale("fr_CA") == "fr"


def test_bcp47_aliases_pt():
    assert resolve_locale("pt_PT") == "pt"


def test_bcp47_aliases_es():
    assert resolve_locale("es_ES") == "es"
    assert resolve_locale("es_MX") == "es"
    assert resolve_locale("es_AR") == "es"


def test_bcp47_aliases_norwegian():
    assert resolve_locale("nb") == "no"
    assert resolve_locale("nn") == "no"
    assert resolve_locale("nb_NO") == "no"


def test_language_subtag_fallback():
    # Uncommon regional codes not in aliases fall back to base language
    assert resolve_locale("de_XX") == "de"
    assert resolve_locale("es_ZZ") == "es"
    assert resolve_locale("it_IT") == "it"


def test_case_insensitive():
    assert resolve_locale("EN") == "en"
    assert resolve_locale("FR") == "fr"
    assert resolve_locale("FR_BE") == "fr_BE"
    assert resolve_locale("PT_BR") == "pt_BR"


def test_unsupported_language_raises():
    with pytest.raises(UnsupportedLanguageError) as exc_info:
        resolve_locale("xx")
    assert "xx" in str(exc_info.value)


def test_unsupported_chinese_raises():
    # zh is not in num2words
    with pytest.raises(UnsupportedLanguageError):
        resolve_locale("zh_CN")


def test_unsupported_basque_raises():
    with pytest.raises(UnsupportedLanguageError):
        resolve_locale("eu")


def test_supported_locales_list():
    langs = SUPPORTED_LOCALES
    assert "en" in langs
    assert "fr" in langs
    assert "fr_BE" in langs
    assert "fr_CH" in langs
    assert "pt_BR" in langs
    assert langs == sorted(langs)
