import json
from typing import AsyncIterator
from pathlib import Path

import aioitertools as aiter
import aiofiles

from fitaudit import TARGET


async def save_json(file, obj):
    data = json.dumps(obj, ensure_ascii=False)
    async with aiofiles.open(TARGET / file, 'w') as f:
        await f.write(data)


async def chunked(seq: str, size: int) -> AsyncIterator[str]:
    for i in ["".join(_) async for _ in aiter.batched(seq, size)]:
        yield i


json_obj = dict | list | str | bytes


async def save_chunked(file: Path, obj: json_obj, size: int):
    data = json.dumps(obj, ensure_ascii=False)
    async with aiofiles.open(TARGET / file, 'w') as f:
        async for chunk in chunked(data, size):
            await f.write(chunk)
