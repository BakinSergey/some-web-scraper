import asyncio


def create_tasks(n, coro, *args):
    return [asyncio.create_task(coro(*args)) for _ in range(n)]


def cancel_tasks(tasks):
    [t.cancel() for t in tasks]
