"""Agent skills call each other only through their invocation contract."""

import re
from pathlib import Path

import pytest

from tests.support.tracked_files import tracked_files

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"
BA_SKILLS = sorted(path for path in SKILLS_DIR.glob("ba-*") if path.is_dir())
INVOCATION_HEADING = re.compile(r"^## Wywołanie\s*$", re.MULTILINE)
SECTION_REFERENCE = re.compile(
    r"\bba-[a-z-]+`?\s+(?:§|krok\s+\d)|krok\s+\d+\s+skilla\s+`?ba-[a-z-]+"
)


@pytest.mark.parametrize("skill_dir", BA_SKILLS, ids=lambda path: path.name)
def test_ba_skill_has_invocation_section(skill_dir: Path) -> None:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

    assert INVOCATION_HEADING.search(text), (
        f"{skill_dir.name}/SKILL.md has no '## Wywołanie' section"
    )


def test_tracked_files_skip_git_ignored_files() -> None:
    ignored = SKILLS_DIR / ".DS_Store"
    created = not ignored.exists()
    if created:
        ignored.write_bytes(b"Bud1\x00\x00\x80\x80")
    try:
        files = tracked_files(SKILLS_DIR)
    finally:
        if created:
            ignored.unlink()

    assert ignored not in files
    assert SKILLS_DIR / "ba-plan" / "SKILL.md" in files


def test_no_skill_references_ba_skill_sections() -> None:
    hits = [
        f"{path.relative_to(REPO_ROOT)}:{number}: {match.group(0)}"
        for path in tracked_files(SKILLS_DIR)
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1)
        for match in SECTION_REFERENCE.finditer(line)
    ]

    assert not hits, (
        "call ba-* skills through their '## Wywołanie' contract, not by section or step:\n"
        + "\n".join(hits)
    )
