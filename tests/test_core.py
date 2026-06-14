import pytest

from alphabetic_sort import alphabetic_sort, get_supported_languages
from alphabetic_sort.exceptions import UnsupportedLanguageError

# ---------------------------------------------------------------------------
# Basic alphabetical sort — English
# ---------------------------------------------------------------------------


def test_basic_en():
    # one, five, twelve → five, one, twelve → [5, 1, 12]
    assert alphabetic_sort([1, 5, 12], "en") == [5, 1, 12]


def test_basic_en_bcp47_hyphen():
    assert alphabetic_sort([1, 5, 12], "en-UK") == [5, 1, 12]


def test_basic_en_bcp47_underscore():
    assert alphabetic_sort([1, 5, 12], "en_US") == [5, 1, 12]


# ---------------------------------------------------------------------------
# Regional variant correctness — French
# ---------------------------------------------------------------------------


def test_fr_BE_vs_fr_different_result():
    # 11=onze, 90=quatre-vingt-dix (fr) vs nonante (fr_BE)
    # fr:    onze(o) < quatre-vingt-dix(q) → [11, 90]
    # fr_BE: nonante(n) < onze(o)          → [90, 11]
    assert alphabetic_sort([11, 90], "fr") == [11, 90]
    assert alphabetic_sort([11, 90], "fr_BE") == [90, 11]


def test_fr_CH_vs_fr_different_result():
    # 11=onze, 80=quatre-vingts (fr) vs huitante (fr_CH)
    # fr:    onze(o) < quatre-vingts(q) → [11, 80]
    # fr_CH: huitante(h) < onze(o)     → [80, 11]
    assert alphabetic_sort([11, 80], "fr") == [11, 80]
    assert alphabetic_sort([11, 80], "fr_CH") == [80, 11]


def test_fr_BE_words_differ_from_fr():
    # Verify intermediate words are genuinely different
    _, orig_fr, _ = alphabetic_sort([70, 80, 90], "fr", return_words=True)
    _, orig_frbe, _ = alphabetic_sort([70, 80, 90], "fr_BE", return_words=True)
    assert orig_fr != orig_frbe


# ---------------------------------------------------------------------------
# Other languages
# ---------------------------------------------------------------------------


def test_basic_de():
    # acht(8), drei(3), eins(1), elf(11), fünf(5), neun(9), sechs(6),
    # sieben(7), vier(4), zehn(10), zwei(2), zwölf(12)
    assert alphabetic_sort(list(range(1, 13)), "de") == [8, 3, 1, 11, 5, 9, 6, 7, 4, 10, 2, 12]


def test_basic_de_bcp47():
    assert alphabetic_sort(list(range(1, 13)), "de_DE") == [8, 3, 1, 11, 5, 9, 6, 7, 4, 10, 2, 12]


def test_basic_fr():
    # un(1), deux(2), trois(3) → deux, trois, un → [2, 3, 1]
    assert alphabetic_sort([1, 2, 3], "fr") == [2, 3, 1]


def test_basic_es():
    # uno(1), dos(2), tres(3), cuatro(4), cinco(5)
    # alpha: cinco, cuatro, dos, tres, uno → [5, 4, 2, 3, 1]
    assert alphabetic_sort([1, 2, 3, 4, 5], "es") == [5, 4, 2, 3, 1]


def test_basic_it():
    # uno(1), due(2), tre(3), quattro(4), cinque(5)
    # alpha: cinque, due, quattro, tre, uno → [5, 2, 4, 3, 1]
    assert alphabetic_sort([1, 2, 3, 4, 5], "it") == [5, 2, 4, 3, 1]


def test_basic_ru():
    result = alphabetic_sort([1, 2, 3], "ru")
    assert sorted(result) == [1, 2, 3]
    assert len(result) == 3


def test_basic_nl():
    result = alphabetic_sort([1, 2, 3, 4, 5], "nl")
    assert len(result) == 5
    assert set(result) == {1, 2, 3, 4, 5}


def test_basic_pt_br():
    result = alphabetic_sort([1, 2, 3], "pt_BR")
    assert len(result) == 3


# ---------------------------------------------------------------------------
# Float support
# ---------------------------------------------------------------------------


def test_floats_basic():
    # one point five (1.5), zero point five (0.5), two point five (2.5)
    # alpha: one... < two... < zero... → [1.5, 2.5, 0.5]
    assert alphabetic_sort([1.5, 0.5, 2.5], "en") == [1.5, 2.5, 0.5]


def test_floats_mixed_with_integers():
    result = alphabetic_sort([1, 1.5, 2], "en")
    assert len(result) == 3
    assert set(result) == {1, 1.5, 2}


def test_integer_types_preserved():
    result = alphabetic_sort([1, 5, 12], "en")
    assert all(isinstance(n, int) for n in result)


def test_float_types_preserved():
    result = alphabetic_sort([1.5, 0.5], "en")
    assert all(isinstance(n, float) for n in result)


# ---------------------------------------------------------------------------
# Negative number rules:
#   - negatives always before non-negatives
#   - negatives sorted in REVERSE alpha of their absolute value word
#   - "minus" word is ignored (abs value used as sort key)
# ---------------------------------------------------------------------------


def test_all_negatives_reverse_alpha():
    # abs words: three(-3), one(-1), two(-2)
    # reverse alpha: two > three > one → [-2, -3, -1]
    assert alphabetic_sort([-3, -1, -2], "en") == [-2, -3, -1]


def test_negatives_before_positives():
    result = alphabetic_sort([-1, 5, -2, 3], "en")
    neg_part = [n for n in result if n < 0]
    pos_part = [n for n in result if n >= 0]
    assert result.index(neg_part[-1]) < result.index(pos_part[0])


def test_mixed_negatives_and_positives():
    # neg abs: five(-5), one(-1), twelve(-12) → reverse: twelve, one, five → [-12, -1, -5]
    # pos: three(3), seven(7) → seven, three → [7, 3]
    # result: [-12, -1, -5, 7, 3]
    assert alphabetic_sort([-5, -1, -12, 3, 7], "en") == [-12, -1, -5, 7, 3]


def test_zero_treated_as_non_negative():
    result = alphabetic_sort([-1, 0, 1], "en")
    assert result[0] == -1
    # 0 and 1 are both non-negative, zero and one → one < zero → [1, 0]
    assert result == [-1, 1, 0]


def test_negative_floats():
    result = alphabetic_sort([-1.5, -0.5, -2.5], "en")
    # abs words: one point five, zero point five, two point five
    # reverse alpha: zero... > two... > one... → [-0.5, -2.5, -1.5]
    assert result == [-0.5, -2.5, -1.5]


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


def test_empty_list():
    assert alphabetic_sort([], "en") == []


def test_single_element():
    assert alphabetic_sort([42], "en") == [42]


def test_single_negative():
    assert alphabetic_sort([-7], "en") == [-7]


def test_duplicates_stable_sort():
    result = alphabetic_sort([1, 1, 2], "en")
    assert result.count(1) == 2
    assert result.count(2) == 1


def test_zero_alone():
    assert alphabetic_sort([0], "en") == [0]


# ---------------------------------------------------------------------------
# return_words=True
# ---------------------------------------------------------------------------


def test_return_words_structure():
    result = alphabetic_sort([1, 5, 12], "en", return_words=True)
    assert isinstance(result, tuple)
    assert len(result) == 3
    sorted_nums, original_words, sorted_words = result
    assert sorted_nums == [5, 1, 12]
    assert len(original_words) == 3
    assert len(sorted_words) == 3


def test_return_words_original_order():
    _, original_words, _ = alphabetic_sort([1, 5, 12], "en", return_words=True)
    # original_words match input order [1, 5, 12] → [one, five, twelve]
    assert original_words == ["one", "five", "twelve"]


def test_return_words_sorted_order():
    _, _, sorted_words = alphabetic_sort([1, 5, 12], "en", return_words=True)
    # sorted order [5, 1, 12] → [five, one, twelve]
    assert sorted_words == ["five", "one", "twelve"]


def test_return_words_empty():
    result = alphabetic_sort([], "en", return_words=True)
    assert result == ([], [], [])


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


def test_unsupported_language_raises():
    with pytest.raises(UnsupportedLanguageError):
        alphabetic_sort([1, 2], "xx")


def test_unsupported_chinese_raises():
    with pytest.raises(UnsupportedLanguageError):
        alphabetic_sort([1, 2], "zh_CN")


def test_non_list_raises_type_error():
    with pytest.raises(TypeError):
        alphabetic_sort((1, 2, 3), "en")  # type: ignore


def test_non_numeric_element_raises_type_error():
    with pytest.raises(TypeError):
        alphabetic_sort([1, "two", 3], "en")  # type: ignore


# ---------------------------------------------------------------------------
# get_supported_languages
# ---------------------------------------------------------------------------


def test_get_supported_languages_includes_core_locales():
    langs = get_supported_languages()
    for lang in ("en", "fr", "fr_BE", "fr_CH", "de", "es", "it", "pt", "pt_BR", "ru", "nl"):
        assert lang in langs, f"{lang} missing from supported languages"


def test_get_supported_languages_is_sorted():
    langs = get_supported_languages()
    assert langs == sorted(langs)


def test_get_supported_languages_no_duplicates():
    langs = get_supported_languages()
    assert len(langs) == len(set(langs))
