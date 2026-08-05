"""Shared pytest fixtures for the OmniForge test suite.

Some test modules run coroutines with `asyncio.run()` (the modern API, which
clears the current event loop when it finishes) while others use the legacy
`asyncio.get_event_loop().run_until_complete()` pattern, which raises on
Python 3.13 once no current loop exists. This autouse fixture reinstalls a
fresh event loop after every test so the suite is order-independent, removing
the need for per-module loop-juggling helpers.
"""

import asyncio

import pytest


@pytest.fixture(autouse=True)
def _reset_event_loop():
    """Ensure a current event loop exists before and after each test."""
    # Install a fresh loop going into the test for legacy get_event_loop() callers.
    asyncio.set_event_loop(asyncio.new_event_loop())
    yield
    # asyncio.run() clears the current loop on exit; leave a fresh one installed
    # so a later test's get_event_loop() call still works.
    asyncio.set_event_loop(asyncio.new_event_loop())
