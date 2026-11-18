"""ba-ship-pr writes scratch files to .ai/scratch/, which git ignores."""

import re
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SHIP_PR_SKILL = REPO_ROOT / "skills/ba-ship-pr/SKILL.md"
SETUP_SKILL = REPO_ROOT / "skills/ba-setup/SKILL.md"
README = REPO_ROOT / "README.md"
GITIGNORE_SECTION = re.compile(r"^## Wpis w \.gitignore\n(.*?)(?=^## )", re.MULTILINE | re.DOTALL)
STEPS = re.compile(r"^## Kroki\n(.*?)(?=^## )", re.MULTILINE | re.DOTALL)
GENERATION_STEP = re.compile(
    r"^4\. \*\*Generowanie\.\*\*(.*?)(?=^\d+\. )", re.MULTILINE | re.DOTALL
)


def test_repo_gitignore_ignores_scratch_dir() -> None:
    git = shutil.which("git")
    assert git, "git is required to check ignored paths"
    result = subprocess.run(  # noqa: S603 - fixed argv built in the test, no external input
        [git, "check-ignore", "-q", ".ai/scratch/reviews/x.patch"],
        cwd=REPO_ROOT,
        check=False,
        timeout=30,
    )

    assert result.returncode == 0, ".gitignore does not ignore .ai/scratch/"


def test_ship_pr_writes_to_ai_scratch() -> None:
    text = SHIP_PR_SKILL.read_text(encoding="utf-8")

    assert "mkdir -p .ai/scratch/reviews" in text
    assert 'snap=".ai/scratch/reviews/pre-ship-pr-' in text
    assert ">> .ai/scratch/reviews/pre-ship-pr-index.txt" in text
    assert ".claude/scratch" not in text


def test_setup_has_gitignore_section() -> None:
    match = GITIGNORE_SECTION.search(SETUP_SKILL.read_text(encoding="utf-8"))
    assert match, "ba-setup has no '## Wpis w .gitignore' section"
    section = match.group(1)

    assert "git check-ignore -q .ai/scratch/x" in section
    assert "`.ai/scratch/`" in section
    assert "kroku 5" in section
    assert "kroku 8" in section


def test_setup_generation_step_points_to_gitignore_section() -> None:
    steps = STEPS.search(SETUP_SKILL.read_text(encoding="utf-8"))
    assert steps, "ba-setup has no '## Kroki' section"
    step = GENERATION_STEP.search(steps.group(1))
    assert step, "ba-setup has no step 4 'Generowanie'"

    assert "§ Wpis w .gitignore" in step.group(1)


def test_readme_mentions_setup_gitignore_entry() -> None:
    text = README.read_text(encoding="utf-8")

    assert "`.ai/scratch/`" in text
