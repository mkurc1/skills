"""ba-ship-pr writes scratch files to .ai/scratch/, which git ignores."""

import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SHIP_PR_SKILL = REPO_ROOT / "skills/ba-ship-pr/SKILL.md"
SETUP_SKILL = REPO_ROOT / "skills/ba-setup/SKILL.md"
README = REPO_ROOT / "README.md"
GITIGNORE_SECTION = re.compile(r"^## Wpis w \.gitignore\n(.*?)(?=^## )", re.MULTILINE | re.DOTALL)
STEPS = re.compile(r"^## Kroki\n(.*?)(?=^## )", re.MULTILINE | re.DOTALL)
BASH_BLOCK = re.compile(r"```bash\n(.*?)```", re.DOTALL)
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
    lines = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()

    assert ".ai/scratch/" in lines, ".gitignore has no '.ai/scratch/' line"
    assert result.returncode == 0, "git does not ignore .ai/scratch/"


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

    assert "git diff --quiet HEAD -- .gitignore" in section
    assert "znakiem nowej linii" in section
    assert "`.ai/scratch/`" in section
    assert "kroku 5" in section
    assert "kroku 8" in section


def test_setup_steps_carry_gitignore_entry_to_commit_and_report() -> None:
    steps = STEPS.search(SETUP_SKILL.read_text(encoding="utf-8"))
    assert steps, "ba-setup has no '## Kroki' section"
    body = steps.group(1)
    step = GENERATION_STEP.search(body)
    assert step, "ba-setup has no step 4 'Generowanie'"

    assert "§ Wpis w .gitignore" in step.group(1)
    assert "plików z dopisanymi sekcjami i zmiany `.gitignore`" in body
    assert "`.gitignore` dodajesz według § Wpis w .gitignore" in body
    assert "- wpis `.ai/scratch/` w `.gitignore`: dopisany albo „wpis już jest”;" in body


def test_readme_mentions_setup_gitignore_entry() -> None:
    lines = README.read_text(encoding="utf-8").splitlines()
    setup_row = next((line for line in lines if line.startswith("| [`ba-setup`]")), None)
    assert setup_row, "README has no ba-setup row"
    rerun = [line for line in lines if "`ba-setup` ponownie" in line]

    assert "`.ai/scratch/`" in setup_row
    assert rerun, "README does not tell configured repos to rerun ba-setup"
    assert "`.ai/scratch/`" in rerun[0]


def _setup_check_block() -> str:
    section = GITIGNORE_SECTION.search(SETUP_SKILL.read_text(encoding="utf-8"))
    assert section, "ba-setup has no '## Wpis w .gitignore' section"
    block = BASH_BLOCK.search(section.group(1))
    assert block, "ba-setup '## Wpis w .gitignore' has no bash block"
    return block.group(1)


@pytest.mark.parametrize(
    ("gitignore", "has_entry"),
    [
        (None, False),
        (".DS_Store\n", False),
        (".ai/\n", False),
        ("!.ai/scratch/\n", False),
        (".DS_Store\n.ai/scratch/\n", True),
        (".ai/scratch/", True),
    ],
    ids=["no-file", "other-rules", "broader-rule", "negation", "entry", "entry-no-newline"],
)
def test_setup_check_block_finds_only_literal_entry(
    tmp_path: Path, gitignore: str | None, has_entry: bool
) -> None:
    bash = shutil.which("bash")
    assert bash, "bash is required to run the ba-setup check block"
    if gitignore is not None:
        (tmp_path / ".gitignore").write_text(gitignore, encoding="utf-8")
    result = subprocess.run(  # noqa: S603 - block comes from a tracked skill file
        [bash, "-c", _setup_check_block()],
        cwd=tmp_path,
        capture_output=True,
        check=False,
        text=True,
        timeout=30,
    )

    assert ("wpis już jest" in result.stdout) is has_entry
