# Katalog roboczy `ba-ship-pr` w `.ai/scratch/` — plan implementacji

Issue: #7

**Cel:** `ba-ship-pr` zapisuje snapshot i raporty w `.ai/scratch/reviews/`. `.gitignore` tego repo ignoruje `.ai/scratch/`. `ba-setup` dopisuje ten wpis do `.gitignore` obcego repo.

**Architektura:** Zmiana mieszka w treści dwóch skilli i w `.gitignore`. Najpierw `.gitignore`, potem `ba-ship-pr`, potem `ba-setup` z `README.md`. Każde zadanie zaczyna od testu w `tests/test_scratch_dir.py`.

Specyfikacja: [`.ai/specs/2026-11-18-ship-pr-scratch-gitignore.md`](2026-11-18-ship-pr-scratch-gitignore.md)

## Ograniczenia globalne

- Ścieżka katalogu roboczego: `.ai/scratch/`. Raporty i snapshot: `.ai/scratch/reviews/`.
- Wpis w `.gitignore`: linia `.ai/scratch/`.
- Nazwa sekcji w `ba-setup`: `## Wpis w .gitignore`.
- Numeracja kroków `ba-setup` zostaje: 7 to „Etykiety spoza konfiguracji”, 8 to „Commit”. Pilnuje tego `tests/test_setup_extra_labels.py`.
- `ba-ship-pr` niczego nie sprawdza i nie zakłada wpisu. Decyzja operatora.
- Wzmianki o `.claude/` w `ba-ship-pr` poza miejscem zapisu zostają: `:240`, `:257`, `:421`, `:437`.
- Skill: `superpowers:writing-skills` przy edycji `SKILL.md`. Testy: agent `python-developer:developer`. Test regresyjny: `ba-mutation-check`.

## Na co uważać

- **Test `.gitignore` zależy od gita.** `git check-ignore` potrzebuje repo. CI ma checkout, więc test działa. Sprawdza to Task 1.
- **`tests/test_skill_portability.py` zabrania nazw projektu w skillach.** Nowa treść nie wspomina `mkurc1` ani Verakio. Sprawdza to bramka w Task 3.

---

### Task 1: wpis `.ai/scratch/` w `.gitignore`

**Pliki:**
- Utwórz: `tests/test_scratch_dir.py`
- Zmień: `.gitignore`

**Interfejsy:**
- Dostarcza: plik testów, który rozszerzają Task 2 i 3.

- [ ] **Krok 1: Test**

```python
"""ba-ship-pr writes scratch files to .ai/scratch/, which git ignores."""

import re
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
```

- [ ] **Krok 2: Uruchom test**

Uruchom: `uv run pytest -p no:cacheprovider tests/test_scratch_dir.py`
Oczekiwany wynik: FAIL, „.gitignore does not ignore .ai/scratch/”.

- [ ] **Krok 3: Kod** — dopisz na końcu `.gitignore`:

```
.ai/scratch/
```

- [ ] **Krok 4: Uruchom test**

Uruchom: `uv run pytest -p no:cacheprovider tests/test_scratch_dir.py`
Oczekiwany wynik: PASS

- [ ] **Krok 5: Commit**

```bash
git add .gitignore tests/test_scratch_dir.py .ai/specs/2026-11-18-ship-pr-scratch-gitignore.md .ai/specs/2026-11-18-ship-pr-scratch-gitignore-plan.md
git commit -m "fix(gitignore): ignoruje katalog roboczy .ai/scratch/ (#7)"
```

---

### Task 2: `ba-ship-pr` zapisuje do `.ai/scratch/reviews/`

**Pliki:**
- Zmień: `tests/test_scratch_dir.py`
- Zmień: `skills/ba-ship-pr/SKILL.md:64`, `:68`, `:74`, `:218`, `:245`

**Interfejsy:**
- Wymaga: `tests/test_scratch_dir.py` z Task 1.

- [ ] **Krok 1: Test** — dopisz do `tests/test_scratch_dir.py`:

```python
SHIP_PR_SKILL = REPO_ROOT / "skills/ba-ship-pr/SKILL.md"


def test_ship_pr_writes_to_ai_scratch() -> None:
    text = SHIP_PR_SKILL.read_text(encoding="utf-8")

    assert "mkdir -p .ai/scratch/reviews" in text
    assert 'snap=".ai/scratch/reviews/pre-ship-pr-' in text
    assert ">> .ai/scratch/reviews/pre-ship-pr-index.txt" in text
    assert ".claude/scratch" not in text
```

Stała `SHIP_PR_SKILL` idzie pod `REPO_ROOT`, test na koniec pliku.

- [ ] **Krok 2: Uruchom test**

Uruchom: `uv run pytest -p no:cacheprovider tests/test_scratch_dir.py`
Oczekiwany wynik: FAIL w `test_ship_pr_writes_to_ai_scratch` na `mkdir -p .ai/scratch/reviews`.

- [ ] **Krok 3: Kod** — w `skills/ba-ship-pr/SKILL.md`:

- `:64`, `:68`, `:74`: zamień `.claude/scratch/reviews` na `.ai/scratch/reviews`.
- `:218` zamień całą linię na:

```markdown
Miejsce zapisu: `.ai/scratch/reviews/`. Katalog `.ai/scratch/` jest w `.gitignore`, więc raporty nie wejdą do commita niezależnie od tego, którą ścieżką skończy się pętla. Wpis w `.gitignore` dodaje skill `ba-setup`.
```

- `:245`: zamień `.claude/scratch/reviews/` na `.ai/scratch/reviews/`.

- [ ] **Krok 4: Uruchom test**

Uruchom: `uv run pytest -p no:cacheprovider tests/test_scratch_dir.py && ! grep -rn ".claude/scratch" skills/`
Oczekiwany wynik: PASS, `grep` bez trafień.

- [ ] **Krok 5: Commit**

```bash
git add skills/ba-ship-pr/SKILL.md tests/test_scratch_dir.py
git commit -m "fix(ba-ship-pr): zapisuje snapshot i raporty w .ai/scratch/ (#7)"
```

---

### Task 3: `ba-setup` dopisuje `.ai/scratch/` do `.gitignore`

**Pliki:**
- Zmień: `tests/test_scratch_dir.py`
- Zmień: `skills/ba-setup/SKILL.md`: linia „Wynik:” (`:8`), tabela „Wywołanie” (`:16`), kroki 4, 5 i 8 (`:47-67`), raport końcowy (`:70-76`), nowa sekcja przed `## Etykiety` (`:93`)
- Zmień: `README.md:39`

**Interfejsy:**
- Wymaga: `tests/test_scratch_dir.py` z Task 2.

- [ ] **Krok 1: Test** — dopisz do `tests/test_scratch_dir.py`:

```python
SETUP_SKILL = REPO_ROOT / "skills/ba-setup/SKILL.md"
README = REPO_ROOT / "README.md"
GITIGNORE_SECTION = re.compile(
    r"^## Wpis w \.gitignore\n(.*?)(?=^## )", re.MULTILINE | re.DOTALL
)
STEPS = re.compile(r"^## Kroki\n(.*?)(?=^## )", re.MULTILINE | re.DOTALL)
GENERATION_STEP = re.compile(r"^4\. \*\*Generowanie\.\*\*(.*?)(?=^\d+\. )", re.MULTILINE | re.DOTALL)


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
```

Stałe idą pod `SHIP_PR_SKILL`, testy na koniec pliku.

- [ ] **Krok 2: Uruchom test**

Uruchom: `uv run pytest -p no:cacheprovider tests/test_scratch_dir.py`
Oczekiwany wynik: FAIL w 3 nowych testach. Pierwszy: „ba-setup has no '## Wpis w .gitignore' section”.

- [ ] **Krok 3: Kod** — w `skills/ba-setup/SKILL.md`:

- `:8` zamień na:

```markdown
Wejście: repozytorium bez kompletu `.ai/config/`. Wynik: 12 plików `.ai/config/` i `.ai/docs/sdlc.md`, wpis `.ai/scratch/` w `.gitignore`, etykiety w repo, etykiety spoza konfiguracji skasowane po zgodzie i propozycja commita.
```

- Tabela „Wywołanie”, kolumna „Co zostawia”: po „Pliki `.ai/config/` i `.ai/docs/sdlc.md` zapisane po akceptacji,” dopisz „wpis `.ai/scratch/` w `.gitignore`,”.
- Krok 4: dopisz punkt na końcu listy:

```markdown
   - Wpis w `.gitignore` przygotowujesz według § Wpis w .gitignore.
```

- Krok 5, pierwsza linia: „Pokaż operatorowi naraz wynik dla plików brakujących, zastępowanych, plików z dopisanymi sekcjami i zmiany `.gitignore`.”
- Krok 8, ostatni punkt: „Do commita dodajesz tylko pliki zapisane w kroku 5, także `.gitignore`.”
- Raport końcowy: po pierwszym punkcie dopisz „- wpis `.ai/scratch/` w `.gitignore`: dopisany albo już był;”.
- Przed `## Etykiety` wstaw sekcję:

````markdown
## Wpis w .gitignore

`ba-ship-pr` zapisuje snapshot i raporty review w `.ai/scratch/`. Pliki z tego katalogu nie mogą wejść do commita. Pilnuje tego wpis `.ai/scratch/` w `.gitignore`.

1. Sprawdź, czy git już ignoruje katalog:

   ```bash
   git check-ignore -q .ai/scratch/x
   ```

   - Kod 0: wpis działa. Nic nie zmieniasz. Raport mówi „wpis już jest”.
2. Inny kod: przygotuj linię `.ai/scratch/` na końcu `.gitignore`. Brak pliku: zakładasz go z tą linią.
3. Podgląd z kroku 5 pokazuje zmianę `.gitignore`. Zapis idzie po tej samej akceptacji co pliki `.ai/config/`.
4. Commit z kroku 8 zabiera `.gitignore` razem z plikami `.ai/config/`.

Wpis powstaje także wtedy, gdy wszystkie pliki z tabeli „Pliki” już istnieją. Repo skonfigurowane wcześniej dostaje go przy ponownym uruchomieniu `ba-setup`.
````

W `README.md:39` zamień opis `ba-setup` na:

```markdown
| [`ba-setup`](skills/ba-setup/SKILL.md) | Zakłada `.ai/config/` i opis procesu dla nowego repozytorium. Dopisuje `.ai/scratch/` do `.gitignore`. Po zgodzie kasuje etykiety spoza konfiguracji. |
```

- [ ] **Krok 4: Uruchom test**

Uruchom: `uv run pytest -p no:cacheprovider tests/test_scratch_dir.py`
Oczekiwany wynik: PASS

- [ ] **Krok 5: Bramka jakości**

Uruchom po kolei: `uv sync --locked`, `uv run ruff check tests/`, `uv run ruff format --check tests/`, `uv run pytest`.
Oczekiwany wynik: każda komenda kończy się kodem 0.

- [ ] **Krok 6: Commit**

```bash
git add skills/ba-setup/SKILL.md README.md tests/test_scratch_dir.py
git commit -m "feat(ba-setup): dopisuje .ai/scratch/ do .gitignore (#7)"
```
