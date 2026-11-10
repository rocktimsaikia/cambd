"""Tests for the offline word cache."""

import importlib
import os
import sys

import pytest

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


@pytest.fixture()
def cache_module(tmp_path, monkeypatch):
    """Import cambd.cache with HOME redirected to a temp dir."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    import cambd.cache as cache_module

    importlib.reload(cache_module)
    cache_module.cache_create()
    return cache_module


def test_cache_round_trip(cache_module):
    definitions = [{"Definition": "a test entry.", "Type": "noun"}]
    cache_module.cache_append("zxq-test-word", definitions)
    assert cache_module.is_cached("zxq-test-word") == definitions


def test_uncached_word_returns_none(cache_module):
    assert cache_module.is_cached("zxq-missing-word") is None


def test_corrupt_cache_entry_returns_none(cache_module):
    """A corrupt cache blob must not crash the lookup with JSONDecodeError."""
    with cache_module.con:
        cache_module.con.execute(
            "INSERT OR REPLACE INTO words VALUES (?, ?)",
            ("zxq-corrupt-word", "not-json{{{"),
        )
    assert cache_module.is_cached("zxq-corrupt-word") is None
