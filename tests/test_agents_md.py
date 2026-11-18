"""AGENTS.md holds the agent work rules, and every reference to its sections resolves."""

import re
from pathlib import Path

from tests.support.tracked_files import tracked_files

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS_MD = REPO_ROOT / "AGENTS.md"
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
CONFIG_FILES = [
    REPO_ROOT / ".ai/config/project.md",
    REPO_ROOT / ".ai/docs/sdlc.md",
]
REQUIRED_SECTIONS = ["Rodzaj zmiany", "Reguły skilli", "Katalog .ai/", "Bramka jakości"]
CHANGE_TABLE_HEADER = "| Rodzaj zmiany | Co przeczytać | Kluczowe reguły |"
CHANGE_KINDS = [
    "skills/*/SKILL.md",
    "skills/ba-setup/references/",
    "tests/",
    ".github/workflows/",
    "README.md",
]
AI_DIRECTORIES = ["`config/`", "`docs/`", "`specs/`", "`runs/`"]
SECTION_REF = re.compile(r"`AGENTS\.md` § ([^)”\n]+)[)”]")
H2 = re.compile(r"^## (.+)$", re.MULTILINE)
TABLE_SEPARATOR = re.compile(r"^\|[\s:|-]+\|$")
DENIAL = "Repo nie ma pliku z regułami pracy agenta"


def _agents_text() -> str:
    assert AGENTS_MD.is_file(), "AGENTS.md is missing at the repository root"
    return AGENTS_MD.read_text(encoding="utf-8")


def _headings() -> list[str]:
    return [heading.strip() for heading in H2.findall(_agents_text())]


def _section(name: str) -> str:
    """Text from ``## {name}`` up to the next ``## `` heading or the end of AGENTS.md."""
    match = re.search(
        rf"^## {re.escape(name)}[ \t]*\n(.*?)(?=^## |\Z)",
        _agents_text(),
        re.MULTILINE | re.DOTALL,
    )
    assert match, f"AGENTS.md has no section '## {name}'"
    return match.group(1)


def test_agents_md_has_required_sections() -> None:
    headings = _headings()

    missing = [name for name in REQUIRED_SECTIONS if name not in headings]

    assert not missing, f"AGENTS.md lacks sections: {missing}"


def test_change_table_covers_every_kind() -> None:
    lines = [line.strip() for line in _section("Rodzaj zmiany").splitlines()]
    assert CHANGE_TABLE_HEADER in lines, "change table header is missing"

    start = lines.index(CHANGE_TABLE_HEADER) + 1
    assert start < len(lines), "change table has no separator row"
    assert TABLE_SEPARATOR.match(lines[start]), "change table has no separator row"
    rows: list[str] = []
    for line in lines[start + 1 :]:
        if not line.startswith("|"):
            break
        rows.append(line)
    first_cells = [row.strip("|").split("|")[0] for row in rows]

    assert len(first_cells) == len(CHANGE_KINDS), f"expected one row per kind, got {first_cells}"
    for cell, kind in zip(first_cells, CHANGE_KINDS, strict=True):
        assert kind in cell, f"row '{cell.strip()}' should name '{kind}'"


def test_ai_directory_section_lists_directories() -> None:
    section = _section("Katalog .ai/")

    missing = [name for name in AI_DIRECTORIES if name not in section]

    assert not missing, f"section 'Katalog .ai/' lacks directories: {missing}"


def test_quality_gate_points_to_project_md() -> None:
    section = _section("Bramka jakości")

    assert ".ai/config/project.md" in section
    assert "uv run" not in section, "gate commands belong in .ai/config/project.md"


def test_agents_md_references_resolve() -> None:
    references = [
        (path.relative_to(REPO_ROOT), name.replace("`", "").strip())
        for path in tracked_files(REPO_ROOT)
        if path.suffix == ".md"
        for name in SECTION_REF.findall(path.read_text(encoding="utf-8"))
    ]
    assert len(references) >= 2, f"expected at least 2 section references, found {references}"

    headings = _headings()
    unresolved = [(str(path), name) for path, name in references if name not in headings]

    assert not unresolved, f"references to missing AGENTS.md sections: {unresolved}"


def test_claude_md_imports_agents_md() -> None:
    assert CLAUDE_MD.is_file(), "CLAUDE.md is missing at the repository root"

    lines = CLAUDE_MD.read_text(encoding="utf-8").splitlines()

    assert "@AGENTS.md" in lines


def test_config_no_longer_denies_agents_md() -> None:
    stale = [
        str(path.relative_to(REPO_ROOT))
        for path in CONFIG_FILES
        if DENIAL in path.read_text(encoding="utf-8")
    ]

    assert not stale, f"files still say the repo has no agent rules file: {stale}"
