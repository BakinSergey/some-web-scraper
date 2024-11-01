"""json utils."""

import json
from pathlib import Path
from typing import AsyncIterator

import aiofiles  # type: ignore
import aioitertools as aiter  # type: ignore

from app import TARGET

json_obj = dict | list | str


async def save_json(file: Path, obj: json_obj) -> None:
    """Json save fn."""
    data = json.dumps(obj, ensure_ascii=False)
    async with aiofiles.open(TARGET / file, "w") as f:
        await f.write(data)


async def chunked(seq: str, size: int) -> AsyncIterator[str]:
    """Json save by chunk fn."""
    for i in ["".join(_) async for _ in aiter.batched(seq, size)]:
        yield i


async def save_chunked(file: Path, obj: json_obj, size: int) -> None:
    """Json save chunked fn."""
    data = json.dumps(obj, ensure_ascii=False)
    async with aiofiles.open(TARGET / file, "w") as f:
        async for chunk in chunked(data, size):
            await f.write(chunk)
