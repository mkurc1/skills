"""Portable skills must not name the project they were written in."""

import re
from pathlib import Path

import pytest

from tests.support.tracked_files import tracked_files

REPO_ROOT = Path(__file__).resolve().parents[1]
SHIP_PR_SKILL = REPO_ROOT / "skills/ba-ship-pr/SKILL.md"
SETUP_DIR = REPO_ROOT / "skills/ba-setup"
TEMPLATE_DIR = SETUP_DIR / "references/config"
PORTABLE_SKILLS = [
    REPO_ROOT / "skills/ba-github-issues",
    REPO_ROOT / "skills/ba-plan",
    REPO_ROOT / "skills/ba-implement",
    REPO_ROOT / "skills/ba-refine-issue",
    REPO_ROOT / "skills/ba-ship-pr",
    REPO_ROOT / "skills/ba-wait-checks",
    REPO_ROOT / "skills/ba-setup",
    REPO_ROOT / "skills/ba-qa",
    REPO_ROOT / "skills/ba-mutation-check",
]
PROJECT_WORDS = re.compile(
    r"verakio|mkurc1|status:|prio:|risk:|\.WA\b|supabase"
    r"|pr_body|risk-rules|importlinter|src/scoring|deployment\.md",
    re.IGNORECASE,
)
GATE_COMMANDS = ["uv run mypy", "npm run test"]
LABEL_TABLE = re.compile(r"^## Skutek każdej etykiety\n(.*?)(?=^## )", re.MULTILINE | re.DOTALL)
COLOR = re.compile(r"^`[0-9a-f]{6}`$")
CONFIG_SKILLS = [
    "ba-github-issues",
    "ba-plan",
    "ba-implement",
    "ba-refine-issue",
    "ba-ship-pr",
    "ba-wait-checks",
    "ba-qa",
    "ba-mutation-check",
]
# Heading pattern of the task-brief script from superpowers:subagent-driven-development.
TASK_BRIEF_HEADING = re.compile(r"^#+[ \t]+Task[ \t]+1([^0-9]|$)", re.MULTILINE)
CONFIG_ROW = re.compile(r"^\| `([\w.-]+\.md)` \|", re.MULTILINE)
CONFIG_SECTION = re.compile(r"^## Konfiguracja\n(.*?)^## ", re.MULTILINE | re.DOTALL)
PROJECT_SECTION_REFS = [
    re.compile(r"„([^”]+)” w `project\.md`"),
    re.compile(r"project\.md`? § „([^”]+)”"),
    re.compile(r"project\.md`? \|? ?§ ([^„.:;,|\n]+?)(?=[.:;,|]|$)", re.MULTILINE),
]
PROJECT_ROW = re.compile(r"^\| `project\.md` \|.*$", re.MULTILINE)
QUOTED = re.compile(r"„([^”]+)”")
H2 = re.compile(r"^## (.+)$", re.MULTILINE)


def _skill_files() -> list[Path]:
    return [path for skill in PORTABLE_SKILLS for path in tracked_files(skill)]


@pytest.mark.parametrize("skill_dir", PORTABLE_SKILLS, ids=lambda p: p.name)
def test_portable_skill_has_no_project_words(skill_dir: Path) -> None:
    assert skill_dir.is_dir(), f"missing skill directory {skill_dir}"
    hits = [
        f"{path.relative_to(REPO_ROOT)}:{number}: {match.group(0)}"
        for path in tracked_files(skill_dir)
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1)
        for match in PROJECT_WORDS.finditer(line)
    ]

    assert not hits, (
        "project-specific words in a portable skill; move them to .ai/config/:\n" + "\n".join(hits)
    )


def test_skills_do_not_copy_gate_commands() -> None:
    copies = [
        f"{path.relative_to(REPO_ROOT)}: {command}"
        for path in _skill_files()
        for command in GATE_COMMANDS
        if command in path.read_text(encoding="utf-8")
    ]

    assert not copies, "quality gate commands belong in .ai/config/project.md:\n" + "\n".join(
        copies
    )


def test_ship_pr_config_files_exist() -> None:
    text = SHIP_PR_SKILL.read_text(encoding="utf-8")
    section = re.search(r"^## Konfiguracja\n(.*?)^## ", text, re.MULTILINE | re.DOTALL)
    assert section, "ba-ship-pr has no '## Konfiguracja' section"

    names = re.findall(r"^\| `([\w.-]+\.md)` \|", section.group(1), re.MULTILINE)
    missing = [name for name in names if not (TEMPLATE_DIR / name).is_file()]

    assert names, "the '## Konfiguracja' table lists no config files"
    assert not missing, f"config templates named by ba-ship-pr are missing: {missing}"


def test_ship_pr_section_references_resolve() -> None:
    text = SHIP_PR_SKILL.read_text(encoding="utf-8")
    references = re.findall(r"([\w-]+\.md)`? § „([^”]+)”", text)
    broken = [
        f"{TEMPLATE_DIR.relative_to(REPO_ROOT)}/{name} § {section}"
        for name, section in references
        if not re.search(
            rf"^#{{2,3}} {re.escape(section)}$",
            (TEMPLATE_DIR / name).read_text(encoding="utf-8"),
            re.MULTILINE,
        )
    ]

    assert references, "ba-ship-pr names no config sections"
    assert not broken, "ba-ship-pr points at config sections that do not exist:\n" + "\n".join(
        broken
    )


def _label_rows(path: Path) -> tuple[list[str], list[list[str]]]:
    section = LABEL_TABLE.search(path.read_text(encoding="utf-8"))
    assert section, f"{path} has no 'Skutek każdej etykiety' section"
    lines = [line for line in section.group(1).splitlines() if line.startswith("|")]
    header = [cell.strip() for cell in lines[0].strip("|").split("|")]
    rows = [[cell.strip() for cell in line.strip("|").split("|")] for line in lines[2:]]
    return header, rows


def test_label_table_has_description_and_color() -> None:
    header, rows = _label_rows(TEMPLATE_DIR / "labels.md")

    assert header == ["Etykieta", "Opis", "Kolor", "Skutek"]
    assert rows
    bad = [row[0] for row in rows if len(row) != 4 or not row[1] or not COLOR.match(row[2])]
    assert not bad, f"label rows without description or color: {bad}"


def _skill_text(name: str) -> str:
    return (REPO_ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")


def _project_sections_named_by_skills() -> set[str]:
    names: set[str] = set()
    for skill in sorted((REPO_ROOT / "skills").glob("ba-*/SKILL.md")):
        text = skill.read_text(encoding="utf-8")
        for pattern in PROJECT_SECTION_REFS:
            names.update(pattern.findall(text))
        for row in PROJECT_ROW.findall(text):
            names.update(QUOTED.findall(row))
    return names


def _config_section(skill: str) -> str:
    section = CONFIG_SECTION.search(_skill_text(skill))
    assert section, f"{skill} has no '## Konfiguracja' section"
    return section.group(1)


def test_every_config_file_has_setup_template() -> None:
    named = {name for skill in CONFIG_SKILLS for name in CONFIG_ROW.findall(_config_section(skill))}
    templates = {path.name for path in TEMPLATE_DIR.glob("*.md")}

    assert named, "skills name no config files"
    assert named <= templates, (
        f"config files named by skills but without a template: {sorted(named - templates)}"
    )


def test_project_md_section_contract() -> None:
    named = _project_sections_named_by_skills()
    template = set(H2.findall((TEMPLATE_DIR / "project.md").read_text(encoding="utf-8")))

    assert len(named) >= 7, f"too few project.md section references found: {sorted(named)}"
    assert named <= template, f"sections named by skills but missing: {sorted(named - template)}"
    assert "Pojedynczy test" in named, "ba-mutation-check must read the single-test command"


def test_missing_config_points_to_setup() -> None:
    texts = {name: _skill_text(name) for name in CONFIG_SKILLS}
    stale = [name for name, text in texts.items() if "repozytorium źródłowego" in text]
    unpointed = [name for name, text in texts.items() if "skill `ba-setup`" not in text]

    assert not stale, f"skills still tell to copy .ai/config/: {stale}"
    assert not unpointed, f"skills do not point to ba-setup: {unpointed}"


VARIANT_MARKER = re.compile(r"^<!-- ba-setup: (wariant (\S+)|koniec wariantu) -->$", re.MULTILINE)
VARIANT_PAIR = re.compile(r"^\s+- `([\w-]+)` albo `([\w-]+)`:", re.MULTILINE)


def test_setup_variant_markers_are_known_and_closed() -> None:
    interview = (SETUP_DIR / "references/interview.md").read_text(encoding="utf-8")
    known = {name for pair in VARIANT_PAIR.findall(interview) for name in pair}
    problems = []
    for path in sorted((SETUP_DIR / "references").rglob("*.md")):
        if path.name == "interview.md":
            continue
        text = path.read_text(encoding="utf-8")
        problems += [
            f"{path.name}: malformed {line!r}"
            for line in text.splitlines()
            if "<!--" in line and "ba-setup" in line and not VARIANT_MARKER.fullmatch(line)
        ]
        open_variant = None
        for _marker, name in VARIANT_MARKER.findall(text):
            if name:
                if open_variant or name not in known:
                    problems.append(f"{path.name}: {name}")
                open_variant = name
            else:
                if not open_variant:
                    problems.append(f"{path.name}: unmatched end")
                open_variant = None
        if open_variant:
            problems.append(f"{path.name}: {open_variant} not closed")

    assert len(known) == 4, f"variant pairs in interview.md: {sorted(known)}"
    assert not problems, f"bad ba-setup variant markers: {problems}"


QA_SKILL = REPO_ROOT / "skills/ba-qa/SKILL.md"
QA_SECTIONS = [
    "Start aplikacji",
    "Adres",
    "Logowanie",
    "Konta testowe",
    "Sprzątanie",
    "Zrzuty ekranu",
    "Testy E2E",
]


def test_qa_config_has_the_contract_sections() -> None:
    assert H2.findall((TEMPLATE_DIR / "qa.md").read_text(encoding="utf-8")) == QA_SECTIONS


def test_qa_skill_section_references_resolve() -> None:
    text = QA_SKILL.read_text(encoding="utf-8")
    named = set(re.findall(r"qa\.md`? § „([^”]+)”", text))
    table_row = re.search(r"^\| `qa\.md` \|.*$", text, re.MULTILINE)
    assert table_row, "ba-qa has no qa.md row in its configuration table"
    named |= set(QUOTED.findall(table_row.group(0)))

    assert named, "ba-qa names no qa.md sections"
    assert named <= set(QA_SECTIONS), f"unknown qa.md sections: {sorted(named - set(QA_SECTIONS))}"


QA_DIFF_FREE = [
    *sorted((REPO_ROOT / "skills/ba-qa").rglob("*.md")),
    TEMPLATE_DIR / "qa-plan-template.md",
]


@pytest.mark.parametrize("path", QA_DIFF_FREE, ids=lambda path: path.name)
def test_qa_plans_from_the_spec_without_a_diff(path: Path) -> None:
    assert "diff" not in path.read_text(encoding="utf-8").lower()


def test_qa_skill_runs_on_any_branch() -> None:
    text = QA_SKILL.read_text(encoding="utf-8")
    config = CONFIG_SECTION.search(text)

    assert config, "ba-qa has no configuration section"
    assert "`project.md`" not in config.group(1)
    assert "gałęzi zadania" not in text
    assert "gałąź zadania" not in text.lower()
    assert "`.ai/specs/implemented/*.md`" in text
    assert "`main`, `master` i `develop`" in text


def test_plan_template_task_heading_matches_task_brief() -> None:
    text = (TEMPLATE_DIR / "plan-template.md").read_text(encoding="utf-8")

    assert TASK_BRIEF_HEADING.search(text.replace("{k}", "1"))


@pytest.mark.parametrize(
    "path",
    [
        TEMPLATE_DIR / "qa-plan-template.md",
        REPO_ROOT / "skills/ba-qa/references/report.md",
    ],
    ids=["plan", "report"],
)
def test_qa_files_have_no_issue_line_that_marks_a_spec(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    assert not re.search(r"^(\*\*)?Issue:", text, re.MULTILINE)


def test_setup_lists_every_config_template() -> None:
    table = _skill_text("ba-setup")
    missing = [
        path.name
        for path in TEMPLATE_DIR.glob("*.md")
        if f"`references/config/{path.name}`" not in table
    ]

    assert not missing, f"templates missing from the ba-setup table: {missing}"


def test_ship_pr_moves_every_file_of_the_spec_pair() -> None:
    lines = SHIP_PR_SKILL.read_text(encoding="utf-8").splitlines()
    moves = [line for line in lines if "git mv" in line and "implemented/" in line]

    assert moves, "ba-ship-pr has no step moving the spec to implemented/"
    assert all(suffix in moves[0] for suffix in ["`-plan`", "`-qa`", "`-qa-report`"])
