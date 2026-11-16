"""ba-ship-pr points its review auditors to the project's code review rules file."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SHIP_PR_SKILL = REPO_ROOT / "skills/ba-ship-pr/SKILL.md"


def test_ship_pr_points_auditors_to_rules_file() -> None:
    text = SHIP_PR_SKILL.read_text(encoding="utf-8")

    assert ".ai/config/code-review.md" in text
