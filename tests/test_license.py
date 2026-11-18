"""The repository is licensed under MIT and says so in every place a reader looks."""

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COPYRIGHT = "Copyright (c) 2026 Michał Kurcewicz"


def test_license_file_has_mit_text_and_copyright() -> None:
    lines = (ROOT / "LICENSE").read_text(encoding="utf-8").splitlines()

    assert lines[0] == "MIT License"
    assert COPYRIGHT in lines
    assert any(line.startswith("Permission is hereby granted, free of charge") for line in lines)


def test_pyproject_declares_mit() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]

    assert project["license"] == "MIT"


def test_readme_has_license_section_linking_the_file() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    _, _, section = readme.partition("\n## Licencja\n")

    assert "[LICENSE](LICENSE)" in section.split("\n## ")[0]
