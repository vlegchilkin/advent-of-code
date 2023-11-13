import os
import shutil
from pathlib import Path

import requests


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
    def __init__(self, year: str, day: str, *, create_roots=True):
        self.year = year
        self.day = day
        self.session_cookie = os.getenv("SESSION")
        self.year_url = f"https://adventofcode.com/{year}"
        self.day_url = f"{self.year_url}/day/{day}"

        self.sources_root = Path(__file__).parent.parent / "solutions" / "python" / "aoc" / f"year_{year}"
        self.resources_root = Path(__file__).parent.parent / "resources" / year / "day" / day
        if create_roots:
            if not self.sources_root.exists():
                self.sources_root.mkdir(exist_ok=True, parents=True)
                self.source("__init__.py").write("")

            self.resources_root.mkdir(exist_ok=True, parents=True)

    def resource(self, name) -> Resource:
        return Resource(self.resources_root / name)

    def source(self, filename) -> Resource:
        return Resource(self.sources_root / filename)

    def request_day(self, action: str = ""):
        return requests.get(self.day_url + action, cookies={"session": self.session_cookie})

    def request_year(self, action: str = ""):
        return requests.get(self.year_url + action, cookies={"session": self.session_cookie})


def slice_content(content: str, from_tags, to_tags) -> list[str]:
    result = []
    last_pos = 0
    while (start_index := content.find(from_tags, last_pos)) >= 0:
        finish_index = content.find(to_tags, last_pos)
        result.append(content[start_index + len(from_tags) : finish_index])
        last_pos = finish_index + len(to_tags)
    return result
