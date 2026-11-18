# Licencja MIT dla repozytorium — plan implementacji

Issue: #10

**Cel:** Repo ma plik `LICENSE` z licencją MIT, pole licencji w `pyproject.toml` i sekcję `## Licencja` w `README.md`.

**Architektura:** Zmiana dotyczy 3 plików w katalogu głównym i 1 nowego testu. Najpierw test, potem pliki.

Specyfikacja: [`.ai/specs/2026-11-18-mit-license.md`](2026-11-18-mit-license.md)

## Ograniczenia globalne

- Wiersz praw autorskich: `Copyright (c) 2026 Michał Kurcewicz`.
- Tekst `LICENSE` to kanoniczny tekst MIT, bez zmian w słowach.
- Pole: `license = "MIT"` w sekcji `[project]`.
- Nagłówek sekcji: `## Licencja`.

## Na co uważać

- **Rozpoznanie przez GitHub.** Test nie sprawdza, czy GitHub rozpozna licencję. Tekst kopiujesz dokładnie z wzorca. Sprawdzenie po merge: `gh api repos/mkurc1/skills --jq .license.spdx_id`.
- **`uv.lock`.** Task 1 krok 4 uruchamia `uv sync --locked`. Ta komenda wykrywa niespójność lockfile'a.

---

### Task 1: Licencja MIT

Dobór skilli: agent `python-developer:developer` dla testu, `ba-mutation-check` dla nowego testu.

**Pliki:**
- Utwórz: `tests/test_license.py`
- Utwórz: `LICENSE`
- Zmień: `pyproject.toml:1-5`
- Zmień: `README.md` (koniec pliku)

**Interfejsy:**
- Wymaga: nic.
- Dostarcza: licencję MIT repozytorium.

- [ ] **Krok 1: Test** — `tests/test_license.py`:

```python
"""The repository is licensed under MIT and says so in every place a reader looks."""

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COPYRIGHT = "Copyright (c) 2026 Michał Kurcewicz"


def test_license_file_has_mit_text_and_copyright() -> None:
    lines = (ROOT / "LICENSE").read_text(encoding="utf-8").splitlines()

    assert lines[0] == "MIT License"
    assert COPYRIGHT in lines
    assert any(line.startswith("Permission is hereby granted, free of charge") for line in lines)


def test_pyproject_declares_mit() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]

    assert project["license"] == "MIT"


def test_readme_has_license_section_linking_the_file() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    _, _, section = readme.partition("\n## Licencja\n")

    assert "[LICENSE](LICENSE)" in section.split("\n## ")[0]
```

- [ ] **Krok 2: Uruchom test**

Uruchom: `uv run pytest -p no:cacheprovider tests/test_license.py`
Oczekiwany wynik: FAIL, 3 testy. Brak `LICENSE`, brak klucza `license`, brak sekcji.

- [ ] **Krok 3: Kod**

`LICENSE`:

```
MIT License

Copyright (c) 2026 Michał Kurcewicz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

`pyproject.toml`, po wierszu `description`:

```toml
license = "MIT"
```

`README.md`, na końcu pliku:

```markdown

## Licencja

Repo jest na licencji MIT. Pełny tekst: [LICENSE](LICENSE).
```

- [ ] **Krok 4: Uruchom test i bramkę**

Uruchom: `uv sync --locked && uv run ruff check tests/ && uv run ruff format --check tests/ && uv run pytest`
Oczekiwany wynik: PASS, `uv.lock` bez zmian.

- [ ] **Krok 5: Commit**

```bash
git add LICENSE pyproject.toml README.md tests/test_license.py .ai/specs/2026-11-18-mit-license.md .ai/specs/2026-11-18-mit-license-plan.md
git commit -m "chore(license): licencja MIT dla repozytorium (#10)"
```
