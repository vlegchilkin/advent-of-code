import inspect
import re
from pathlib import Path
from typing import Union, Iterator, Any
from addict import Dict

from ttp import ttp

RESOURCES_ROOT = Path(__file__).parent / "resources"
DAY_SOURCE_REG = re.compile(r"^.*day_(\d+).py$")


def to_int_list(data, sep=","):
    return [int(el) for el in data.split(sep)], None


def to_optional_int(data, no_value="old"):
    if data == no_value:
        return None, None

    return int(data), None


def parse_with_template(text: str, ttp_template: str) -> list[Dict]:
    parser = ttp(data=text, template=ttp_template)
    parser.add_function(to_int_list, scope='match')
    parser.add_function(to_optional_int, scope='match')
    parser.parse()
    objects = parser.result(structure="flat_list")
    return [Dict(obj) for obj in objects]


class Input:

    def __init__(self, test_case: Union[str, int] = 'task'):
        caller_filename = inspect.stack()[1].filename
        day = DAY_SOURCE_REG.match(caller_filename).groups()[0]
        with open(RESOURCES_ROOT / day / f"{test_case}.in", "r") as file:
            self._text = file.read()

    def get_lines(self) -> list[str]:
        return self._text.splitlines()

    def get_iter(self) -> Iterator[str]:
        return iter(self.get_lines())

    def get_objects(self, ttp_template: str) -> list[Dict]:
        return parse_with_template(self._text, ttp_template)

    def get_lists(self, ttp_template: str) -> list[list[Any]]:
        objects = self.get_objects(ttp_template)
        return [list(o.values()) for o in objects]

    def get_text(self) -> str:
        return self._text
