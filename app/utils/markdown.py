"""Markdown doc generation."""

import json
import os
from typing import Dict, List, Union

from markdown_table_generator import (
    generate_markdown,
    table_from_string_list,
)

from app import PROJECT

queries: Dict[str, List[Union[int, None]]] = {
    "getPostman": [
        2002,
    ],
    "listPostmen": [
        None,
    ],
    "getRole": [2002],
    "listRole": [
        None,
    ],
    "getTask": [2002],
    "listTask": [
        None,
    ],
    "getStorehouseSearch": [1000, 3201],
    "getWarehouseSearch": [1000, 3001],
}

mutations: Dict[str, List[Union[int, None]]] = {
    "taskCreate": [
        2002,
    ],
    "taskAddGood": [
        2001,
        2002,
        4004,
    ],
    "taskStart": [1000, 2001, 2002, 3401, 4001, 4002, 4004],
    "taskCancel": [2001, 2002, 4001, 4004],
    "taskFinish": [2001, 2002, 4001, 4004],
    "taskCloseRpoResults": [2002, 4001],
    "taskAddRpoByPostmove": [2002, 4001, 4004],
    "taskAddRpoByBarcode": [2002, 4001, 4004],
    "taskDeleteRpo": [2002, 4001],
    "taskDeleteNotice": [2002, 4001],
    "taskDeleteRposAndNotices": [2002, 4001],
    "taskAddRpoResult": [2002, 4004],
    "taskAddGoodsResult": [2001, 2002, 4001, 4004],
    "taskSetRpoClientType": [2001, 2002, 4001, 4004],
}

bg_tasks: Dict[str, List[Union[int, None]]] = {}


def api_errors_mapping_as_md_table(src: Dict[str, List[int]]) -> str:
    """Markdown table."""
    data = [[k, ", ".join(str(i) for i in v)] for k, v in src.items()]
    data.insert(0, ["эндпоинт", "коды ошибок"])
    table_data = table_from_string_list(data)

    return generate_markdown(table_data)


def api_errors_as_md_table() -> str:
    """Markdown table."""
    with open(PROJECT / "errors" / "errors.json", "r") as f:
        api_errors = json.load(f)

    headers = [str(h) for h in api_errors[0]]
    datarows = [[str(i[h]) for h in headers] for i in api_errors]
    datarows.sort(key=lambda i: i[headers.index("code")])
    datarows.insert(0, headers)

    table_data = table_from_string_list(datarows)
    return generate_markdown(table_data)


def doc_header(title: str, share: bool, space: str, ancestor_id: int):
    """Markdown table."""
    return f"""---
title: {title}
wiki:
   share: {str(share).lower()}
   space: {space}
   ancestor_id: {ancestor_id}
---
"""


def create_api_errors_md_file():
    """Markdown table."""
    title = "Ошибки сервиса"
    share = True
    space = "EASPlat"
    ancestor_id = 474188746  # Варианты ошибок в сервисе Почтальон (класификация)

    with open(
        os.path.join(PROJECT / "docs" / "data.md"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(doc_header(title, share, space, ancestor_id))
        f.write("\n")
        f.write("# Список API ошибок сервиса ")
        f.write("\n")
        f.write(api_errors_as_md_table())
        f.write("\n")
        f.write("# Маппинг API ошибок")
        f.write("\n")
        f.write(api_errors_mapping_as_md_table(queries))
        f.write("\n")
        f.write("## GraphQL Mutations")
        f.write("\n")
        f.write(api_errors_mapping_as_md_table(mutations))
        f.write("\n")
        f.write("## Background Tasks")
        f.write("\n")
        f.write(api_errors_mapping_as_md_table(bg_tasks))


if __name__ == "__main__":
    create_api_errors_md_file()
