"""ba-ship-pr writes scratch files to .ai/scratch/, which git ignores."""

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SHIP_PR_SKILL = REPO_ROOT / "skills/ba-ship-pr/SKILL.md"


def test_repo_gitignore_ignores_scratch_dir() -> None:
    result = subprocess.run(
        ["git", "check-ignore", "-q", ".ai/scratch/reviews/x.patch"],
        cwd=REPO_ROOT,
        check=False,
    )

    assert result.returncode == 0, ".gitignore does not ignore .ai/scratch/"


def test_ship_pr_writes_to_ai_scratch() -> None:
    text = SHIP_PR_SKILL.read_text(encoding="utf-8")

    assert "mkdir -p .ai/scratch/reviews" in text
    assert 'snap=".ai/scratch/reviews/pre-ship-pr-' in text
    assert ">> .ai/scratch/reviews/pre-ship-pr-index.txt" in text
    assert ".claude/scratch" not in text
