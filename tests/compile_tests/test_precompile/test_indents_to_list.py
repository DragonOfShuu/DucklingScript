import pytest
from ....ducklingscript.compiler.errors import InvalidTabError
from ducklingscript.compiler.tab_parse import discover_tab_char, has_tab, parse_document


def test_discover_tab_char():
    """
    Test the discover_tab_char function.
    """
    assert discover_tab_char("    TEXT") == "    "
    assert discover_tab_char("\t\tTEXT") == "\t\t"
    assert discover_tab_char("  \tTEXT") == "  \t"
    assert discover_tab_char("  TEXT") == "  "
    assert discover_tab_char("\tTEXT") == "\t"

def test_discover_tab_char_no_tabs():
    """
    Test the discover_tab_char function with no tabs.
    """
    assert discover_tab_char("TEXT") == ""

def test_discover_tab_char_no_text():
    """
    Test the discover_tab_char function with no text.
    """
    assert discover_tab_char("    ") == ""
    assert discover_tab_char("\t\t") == ""
    assert discover_tab_char("  \t") == ""
    assert discover_tab_char("  ") == ""
    assert discover_tab_char("\t") == ""

def test_has_tab():
    """
    Test the has_tab function.
    """
    assert has_tab("    TEXT", "    ", 1) is True
    assert has_tab("\t\tTEXT", "\t\t", 1) is True
    assert has_tab("  \tTEXT", "  \t", 1) is True
    assert has_tab("  TEXT", "  ", 1) is True
    assert has_tab("\tTEXT", "\t", 1) is True
    assert has_tab("TEXT", None, 1) is False

def test_has_tab_invalid():
    """
    Test the has_tab function with invalid inputs.
    """
    with pytest.raises(InvalidTabError):
        has_tab("    TEXT", "  ", 1)
    
    with pytest.raises(InvalidTabError):
        has_tab("\t\tTEXT", "\t", 1)

def test_has_tab_no_tabs():
    """
    Test the has_tab function with no tabs.
    """
    assert has_tab("TEXT", None, 1) is False
    assert has_tab("    TEXT", None, 1) == "    "
    assert has_tab("\t\tTEXT", None, 1) == "\t\t"
    assert has_tab("  \tTEXT", None, 1) == "  \t"
    assert has_tab("  TEXT", None, 1) == "  "
    assert has_tab("\tTEXT", None, 1) == "\t"
    
