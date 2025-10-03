import pytest
from src.app.detect import detect_type

def test_known_extension_txt():
    t, method = detect_type("example.txt", b"Hello world")
    assert "Text" in t
    assert "extension" in method

def test_magic_bytes_png():
    # PNG signature: 89 50 4E 47 0D 0A 1A 0A
    png_sig = bytes([0x89,0x50,0x4E,0x47,0x0D,0x0A,0x1A,0x0A]) + b"rest"
    t, method = detect_type("noext", png_sig)
    assert "png" in t.lower() or "image" in t.lower()


def test_text_heuristic():
    t, method = detect_type("file.unknown", b"Just some plain ascii text")
    assert "Text" in t or "Plain" in t
