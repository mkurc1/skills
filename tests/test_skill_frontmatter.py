"""Every SKILL.md starts with YAML front matter that strict parsers accept."""

from pathlib import Path

import pytest
import yaml

SKILLS_DIR = Path(__file__).resolve().parents[1] / "skills"
SKILLS = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())


def _front_matter(skill_dir: Path) -> str:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{skill_dir.name}/SKILL.md has no front matter"
    return text.split("---\n", 2)[1]


def test_there_are_eleven_skills() -> None:
    assert len(SKILLS) == 11


@pytest.mark.parametrize("skill_dir", SKILLS, ids=lambda path: path.name)
def test_front_matter_parses_as_yaml(skill_dir: Path) -> None:
    meta = yaml.safe_load(_front_matter(skill_dir))

    assert meta["name"] == skill_dir.name
    assert isinstance(meta["description"], str)
    assert meta["description"].strip()
