"""ba-ship-pr writes scratch files to .ai/scratch/, which git ignores."""

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_repo_gitignore_ignores_scratch_dir() -> None:
    result = subprocess.run(
        ["git", "check-ignore", "-q", ".ai/scratch/reviews/x.patch"],
        cwd=REPO_ROOT,
        check=False,
    )

    assert result.returncode == 0, ".gitignore does not ignore .ai/scratch/"
