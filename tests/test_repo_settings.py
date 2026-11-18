"""Shared editor and git settings live in the repository root."""

import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CRLF = re.compile(r"\b[iw]/(crlf|mixed)\b")
SECTION = re.compile(r"^\[(?P<glob>[^\]]+)\]\n(?P<body>.*?)(?=^\[|\Z)", re.MULTILINE | re.DOTALL)


def _editorconfig() -> dict[str, dict[str, str]]:
    text = (REPO_ROOT / ".editorconfig").read_text(encoding="utf-8")
    sections: dict[str, dict[str, str]] = {}
    for match in SECTION.finditer(text):
        pairs = (
            line.split("=", 1)
            for line in match.group("body").splitlines()
            if "=" in line and not line.lstrip().startswith(("#", ";"))
        )
        sections[match.group("glob")] = {key.strip(): value.strip() for key, value in pairs}
    return sections


def test_editorconfig_is_root() -> None:
    text = (REPO_ROOT / ".editorconfig").read_text(encoding="utf-8")
    assert re.search(r"^root = true$", text, re.MULTILINE)


def test_editorconfig_defaults_to_lf_utf8() -> None:
    defaults = _editorconfig()["*"]
    assert defaults["end_of_line"] == "lf"
    assert defaults["charset"] == "utf-8"
    assert defaults["insert_final_newline"] == "true"
    assert defaults["trim_trailing_whitespace"] == "true"


@pytest.mark.parametrize(
    ("glob", "indent_size", "max_line_length"),
    [
        ("*.md", None, "off"),
        ("*.py", "4", "100"),
        ("*.{yml,yaml}", "2", "off"),
        ("*.toml", "4", "off"),
        ("*.json", "2", "off"),
    ],
)
def test_editorconfig_sets_indent_per_file_type(
    glob: str, indent_size: str | None, max_line_length: str
) -> None:
    section = _editorconfig()[glob]
    assert section["indent_style"] == "space"
    assert section.get("indent_size") == indent_size
    assert section["max_line_length"] == max_line_length


def test_gitattributes_forces_lf_and_marks_png_binary() -> None:
    lines = (REPO_ROOT / ".gitattributes").read_text(encoding="utf-8").splitlines()
    assert "* text=auto eol=lf" in lines
    assert "*.png binary" in lines


def test_gitignore_skips_local_agent_files() -> None:
    lines = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert "CLAUDE.local.md" in lines
    assert ".worktrees/" in lines


def test_no_tracked_file_has_crlf() -> None:
    git = shutil.which("git")
    assert git, "git is required to list tracked files"
    listing = subprocess.run(  # noqa: S603 - fixed argv, no external input
        [git, "ls-files", "--eol"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=True,
        text=True,
        timeout=30,
    ).stdout
    crlf = [line for line in listing.splitlines() if CRLF.search(line.split("\t")[0])]
    assert crlf == []
