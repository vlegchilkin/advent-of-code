import importlib
import os
import re
from pathlib import Path

import pytest

from aoc import Input

RESOURCES_ROOT = Path(__file__).parent.parent / "resources"
DAY_SOURCE_REG = re.compile(r"^.*/(\d+)/day/(\d+)$")


def get_test_cases():
    results = []
    for root, dirs, file_names in sorted(os.walk(RESOURCES_ROOT)):
        if matcher := DAY_SOURCE_REG.match(root):
            year, day = matcher.groups()
            for file_name in file_names:
                if file_name.endswith(".out"):
                    test_case = file_name[:-4]
                    results.append((int(year), int(day), test_case))
    return sorted(results)


def class_for_name(module_name, class_name):
    m = importlib.import_module(module_name)
    c = getattr(m, class_name)
    return c


@pytest.mark.parametrize("year, day, test_case", get_test_cases())
def test_aoc(year, day, test_case):
    clazz = class_for_name(f"aoc.year_{year}.day_{day}", "Solution")
    solution = clazz(Input(test_case, year, day))
    if hasattr(solution, "part_a_b"):
        print(solution.part_a_b())
    else:
        print(solution.part_a())
        print(solution.part_b())
