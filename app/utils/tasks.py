"""AsyncIO tasks utils."""

import asyncio


def create_tasks(n, coro, *args):
    """Create AsyncIO tasks."""
    return [asyncio.create_task(coro(*args)) for _ in range(n)]


def cancel_tasks(tasks):
    """Cancel given AsyncIO tasks."""
    [t.cancel() for t in tasks]
