import html
import os
import shutil
import sys
from pathlib import Path
from markdownify import markdownify as md

import requests as requests

from utils import day_template
from utils.html_parser import AoCHTMLParser


class Resource:
    def __init__(self, path):
        self.path = path

    def exists(self) -> bool:
        return os.path.exists(self.path)

    def write(self, content):
        with open(self.path, "w") as out_f:
            out_f.write(content)

    def read(self) -> str:
        with open(self.path, "r") as in_f:
            return in_f.read()

    def copy(self, src_path):
        shutil.copyfile(src_path, self.path)


class Context:
    def __init__(self, year: str, day: str):
        self.formatted_day = f"{int(day):02d}"
        self.session_cookie = os.getenv("SESSION")
        self.base_url = f"https://adventofcode.com/{year}/day/{day}"
        self.sources_root = Path(__file__).parent.parent / f"aoc_{year}"
        self.resources_root = self.sources_root / "resources" / self.formatted_day
        self.resources_root.mkdir(exist_ok=True, parents=True)

    def resource(self, name) -> Resource:
        return Resource(self.resources_root / name)

    def source(self) -> Resource:
        return Resource(self.sources_root / f"day_{self.formatted_day}.py")

    def request(self, action: str = ""):
        return requests.get(self.base_url + action, cookies={"session": self.session_cookie})


def slice_content(content: str, from_tags, to_tags) -> list[str]:
    result = []
    last_pos = 0
    while (start_index := content.find(from_tags, last_pos)) >= 0:
        finish_index = content.find(to_tags, last_pos)
        result.append(content[start_index + len(from_tags) : finish_index])
        last_pos = finish_index + len(to_tags)
    return result


if __name__ == "__main__":
    context = Context(*sys.argv[1:])

    if not (source_file := context.source()).exists():
        source_file.copy(day_template.__file__)

    if not (input_file := context.resource("puzzle.in")).exists():
        resp = context.request("/input")
        if resp.status_code < 300:
            input_file.write(resp.text)
        else:
            print(resp.text)
            exit(0)

    r_src = context.request()
    page = r_src.text
    main_content = slice_content(page, "<main>", "</main>")[0].strip()

    if not (readme_file := context.resource("README.md")).exists():
        readme_file.write(md(main_content[: main_content.find('<p class="day-success">')]))

    for i, pre_content in enumerate(slice_content(main_content, "<pre><code>", "</code></pre>")):
        if not (input_i_file := context.resource(f"{i}.in")).exists():
            unescaped = html.unescape(pre_content)
            parser = AoCHTMLParser()
            parser.feed(unescaped)
            input_i_file.write(parser.output)
