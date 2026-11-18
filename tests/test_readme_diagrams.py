"""README embeds the process diagrams, and every diagram keeps its Mermaid source."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
DIAGRAMS_DIR = ROOT / "docs" / "diagrams"
DIAGRAMS = [
    "01-dwie-drogi",
    "02-fix-issue-tory",
    "03-decyzje-operatora",
    "04-klocki-i-lancuchy",
]
IMAGE = re.compile(r"!\[[^\]]+\]\((docs/diagrams/[^)]+\.png)\)")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def test_readme_embeds_every_diagram_in_order() -> None:
    embedded = IMAGE.findall(README.read_text(encoding="utf-8"))

    assert embedded == [f"docs/diagrams/{name}.png" for name in DIAGRAMS]


@pytest.mark.parametrize("name", DIAGRAMS)
def test_diagram_has_source_and_png(name: str) -> None:
    assert (DIAGRAMS_DIR / f"{name}.mmd").is_file()
    assert (DIAGRAMS_DIR / f"{name}.png").read_bytes()[:8] == PNG_SIGNATURE
