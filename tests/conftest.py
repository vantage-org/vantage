from pathlib import Path

import yaml


def pytest_generate_tests(metafunc):
    if "case" in metafunc.fixturenames:
        cases = []
        names = []
        for case in Path("./tests/cases/").glob("**/*.yml"):
            with case.open() as f:
                details = yaml.load(f, Loader=yaml.SafeLoader)
                cases.append(details)
                name = []
                parent = case
                while str(parent.stem) != "cases":
                    name.append(str(parent.stem))
                    parent = parent.parent
                names.append("-".join(reversed(name)))
        metafunc.parametrize("case", cases, ids=names)
