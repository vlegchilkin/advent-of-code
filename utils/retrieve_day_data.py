import html
import os
from os.path import exists
from pathlib import Path

import requests as requests

from utils.html_parser import AoCHTMLParser

YEAR = 2022
DAY = 10

SERVER_TASK_PATH = f"https://adventofcode.com/{YEAR}/day/{DAY}"
SERVER_TASK_INPUT_PATH = f"{SERVER_TASK_PATH}/input"
RESOURCES_ROOT = Path(__file__).parent.parent / f"aoc_{YEAR}" / "resources" / f"{DAY:02d}"
SESSION = os.getenv("SESSION")


def _request(url):
    return requests.get(
        url,
        cookies={
            "session": SESSION,
        }
    )


def slice_content(content: str, from_tags, to_tags) -> list[str]:
    result = []
    last_pos = 0
    while (start_index := content.find(from_tags, last_pos)) >= 0:
        finish_index = content.find(to_tags, last_pos)
        result.append(content[start_index + len(from_tags):finish_index])
        last_pos = finish_index + len(to_tags)
    return result


def write(path, content):
    with open(path, 'w') as out_f:
        out_f.write(content)


if __name__ == "__main__":
    RESOURCES_ROOT.mkdir(exist_ok=True)
    if not exists(input_b_path := RESOURCES_ROOT / "task.in"):
        r_b = _request(SERVER_TASK_INPUT_PATH)
        write(input_b_path, r_b.text)

    if not exists(src_path := RESOURCES_ROOT / "task.html"):
        r_src = _request(SERVER_TASK_PATH)
        page = r_src.text
        main_content = slice_content(page, "<main>", "</main>")[0].strip()
        write(src_path, main_content)
    else:
        with open(src_path, "r") as f:
            main_content = f.read()

    for i, pre_content in enumerate(slice_content(main_content, "<pre><code>", "</code></pre>")):
        if not exists(input_a_path := RESOURCES_ROOT / f"{i}.in"):
            unescaped = html.unescape(pre_content)
            parser = AoCHTMLParser()
            parser.feed(unescaped)
            write(input_a_path, parser.output)
