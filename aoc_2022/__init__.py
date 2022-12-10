import inspect
import re
from pathlib import Path
from typing import Union, Iterator

RESOURCES_ROOT = Path(__file__).parent / "resources"
DAY_SOURCE_REG = re.compile(r"^.*day_(\d+).py$")


def get_input_lines(test_case: Union[str, int] = 'task', *, caller_filename=None) -> list[str]:
    if not caller_filename:
        caller_filename = inspect.stack()[1].filename
    day = DAY_SOURCE_REG.match(caller_filename).groups()[0]
    with open(RESOURCES_ROOT / day / f"{test_case}.in", "r") as file:
        return file.read().splitlines()


def get_input_iter(test_case: Union[str, int] = 'task') -> Iterator[str]:
    caller_filename = inspect.stack()[1].filename
    return iter(get_input_lines(test_case, caller_filename=caller_filename))
