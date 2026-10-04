import pytest
from app.preprocessing.unicode_utils import normalize_unicode, is_indic_character, detect_primary_script
from app.preprocessing.cleaner import TextCleaner
from app.preprocessing.tokenizer import Tokenizer


def test_unicode_normalization():
    raw_text = "కృత్రిమ మేధస్సు"
    norm_text = normalize_unicode(raw_text, form="NFC")
    assert norm_text == raw_text
    assert is_indic_character("క") is True
    assert is_indic_character("A") is False
    assert detect_primary_script("కంప్యూటర్") == "Telugu"
    assert detect_primary_script("कंप्यूटर") == "Devanagari"


def test_text_cleaner():
    cleaner = TextCleaner()
    html_text = "<h1>కంప్యూటర్</h1> <p>భాష https://example.com [[వికీపీడియా|లింక్]]</p>"
    cleaned = cleaner.clean(html_text)
    assert "<" not in cleaned
    assert "https" not in cleaned
    assert "కంప్యూటర్" in cleaned
    assert "భాష" in cleaned
    assert "లింక్" in cleaned


def test_unicode_tokenizer():
    tokenizer = Tokenizer()
    text = "కృత్రిమ మేధస్సు అనేది ఆధునిక సాంకేతిక పరిజ్ఞానం."
    tokens = tokenizer.tokenize(text)
    expected = ["కృత్రిమ", "మేధస్సు", "అనేది", "ఆధునిక", "సాంకేతిక", "పరిజ్ఞానం"]
    assert tokens == expected
