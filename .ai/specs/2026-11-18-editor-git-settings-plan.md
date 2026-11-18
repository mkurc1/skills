# Wspólne ustawienia edytora i gita w repo — plan implementacji

Issue: #11

**Cel:** Repo ma `.editorconfig`, `.gitattributes` z LF i dwa nowe wpisy w `.gitignore`. Test pilnuje wszystkich trzech plików i braku CRLF.

**Architektura:** Trzy pliki konfiguracji w katalogu głównym. Najpierw test, potem pliki.

Specyfikacja: [`.ai/specs/2026-11-18-editor-git-settings.md`](2026-11-18-editor-git-settings.md)

## Ograniczenia globalne

- Wartości `.editorconfig` z tabeli w specyfikacji, § Projekt.
- `.gitattributes` ma dokładnie dwie reguły: `* text=auto eol=lf` i `*.png binary`.
- Nowe wpisy `.gitignore`: `CLAUDE.local.md`, `.worktrees/`. Bez `.claude/scratch/`.
- Skille: agent `python-developer:developer` dla testu, `ba-mutation-check` po teście.

## Na co uważać

- **Renormalizacja.** Po dodaniu `.gitattributes` uruchom `git add --renormalize .`. Zmiana w indeksie znaczy, że jakiś plik miał CRLF. Sprawdza Task 2, krok 4.
- **Test na treść.** Test nie sprawdza zachowania edytora. Raport PR-a to mówi.

---

### Task 1: Test ustawień repo

**Pliki:**
- Utwórz: `tests/test_repo_settings.py`

**Interfejsy:**
- Dostarcza: test, który Task 2 robi zielonym.

- [ ] **Krok 1: Test**

```python
"""Shared editor and git settings live in the repository root."""

import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
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
        ("*.md", "2", "off"),
        ("*.py", "4", "100"),
        ("*.{yml,yaml}", "2", "off"),
        ("*.toml", "4", "off"),
        ("*.json", "2", "off"),
    ],
)
def test_editorconfig_sets_indent_per_file_type(
    glob: str, indent_size: str, max_line_length: str
) -> None:
    section = _editorconfig()[glob]
    assert section["indent_style"] == "space"
    assert section["indent_size"] == indent_size
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
    crlf = [line for line in listing.splitlines() if "crlf" in line.split("\t")[0]]
    assert crlf == []
```

- [ ] **Krok 2: Uruchom test**

Uruchom: `uv run pytest -p no:cacheprovider tests/test_repo_settings.py`
Oczekiwany wynik: FAIL. `FileNotFoundError` dla `.editorconfig` i `.gitattributes`, brak wpisów w `.gitignore`. `test_no_tracked_file_has_crlf` przechodzi.

- [ ] **Krok 3: Commit**

```bash
git add tests/test_repo_settings.py .ai/specs/2026-11-18-editor-git-settings.md .ai/specs/2026-11-18-editor-git-settings-plan.md
git commit -m "test(repo): pilnuje ustawień edytora i gita (#11)"
```

### Task 2: Pliki ustawień

**Pliki:**
- Utwórz: `.editorconfig`
- Utwórz: `.gitattributes`
- Zmień: `.gitignore:5`

**Interfejsy:**
- Wymaga: test z Task 1.

- [ ] **Krok 1: `.editorconfig`**

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
indent_style = space
indent_size = 2
max_line_length = off

[*.py]
indent_style = space
indent_size = 4
max_line_length = 100

[*.{yml,yaml}]
indent_style = space
indent_size = 2
max_line_length = off

[*.toml]
indent_style = space
indent_size = 4
max_line_length = off

[*.json]
indent_style = space
indent_size = 2
max_line_length = off
```

- [ ] **Krok 2: `.gitattributes`**

```
* text=auto eol=lf
*.png binary
```

- [ ] **Krok 3: `.gitignore`** — dopisz na końcu:

```
CLAUDE.local.md
.worktrees/
```

- [ ] **Krok 4: Renormalizacja**

Uruchom: `git add --renormalize . && git status --short`
Oczekiwany wynik: zmienione tylko `.editorconfig`, `.gitattributes`, `.gitignore`.

- [ ] **Krok 5: Uruchom test**

Uruchom: `uv run pytest -p no:cacheprovider tests/test_repo_settings.py`
Oczekiwany wynik: PASS

- [ ] **Krok 6: Mutacja** — skill `ba-mutation-check`. Usuń `*.png binary` i `.worktrees/`, test pada. Przywróć.

- [ ] **Krok 7: Bramka jakości** — komendy z `.ai/config/project.md` § Bramka jakości. Wszystkie przechodzą.

- [ ] **Krok 8: Commit**

```bash
git add .editorconfig .gitattributes .gitignore
git commit -m "chore(repo): wspólne ustawienia edytora i gita (#11)"
```
