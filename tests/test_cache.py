import pytest
import time

from sdlg._cache import _Cache

def test_cache_set_and_get():
    cache = _Cache()
    cache.set("test_key", "test_value")
    assert cache.get("test_key") == "test_value"

def test_cache_expiry():
    cache = _Cache()
    cache.lifespan = 1  # Set short lifespan for testing
    cache.set("test_key", "test_value")
    time.sleep(1.1)  # Wait for expiry
    assert cache.get("test_key") is None

def test_cache_persistence_with_save():
    cache = _Cache()
    cache.lifespan = 1
    cache.set("test_key", "test_value", save=True)
    time.sleep(1.1)
    assert cache.get("test_key") == "test_value"  # Should persist due to 'save'

def test_cache_callback_on_expiry():
    cache = _Cache()
    cache.lifespan = 1
    callback_called = []

    def callback(value):
        callback_called.append(value)

    cache.set("test_key", "test_value", callback=callback)
    time.sleep(1.1)
    cache.get("test_key")  # Trigger expiry check
    assert callback_called == ["test_value"]  # Callback should be called

def test_cache_overwrite():
    cache = _Cache()
    cache.set("test_key", "initial_value")
    cache.set("test_key", "new_value")
    assert cache.get("test_key") == "new_value"
