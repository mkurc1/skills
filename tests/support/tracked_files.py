"""Files tracked by git, for tests that check repository content."""

import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def tracked_files(directory: Path) -> list[Path]:
    """Files under ``directory`` tracked by git; ignored files such as .DS_Store stay out."""
    git = shutil.which("git")
    assert git, "git is required to list tracked files"
    listing = subprocess.run(  # noqa: S603 - fixed argv built in the test, no external input
        [git, "ls-files", "-z", "--", str(directory)],
        cwd=REPO_ROOT,
        capture_output=True,
        check=True,
        text=True,
        timeout=30,
    ).stdout
    paths = (REPO_ROOT / name for name in listing.split("\0") if name)
    return sorted(path for path in paths if path.is_file())
