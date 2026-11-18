# `ba-setup` pyta o skasowanie etykiet spoza konfiguracji — plan implementacji

Issue: #5

**Cel:** `ba-setup` ma krok 7, który wypisuje etykiety spoza konfiguracji z liczbą użyć i kasuje je tylko po zgodzie operatora.

**Architektura:** Reguła mieszka w nowej sekcji `## Etykiety spoza konfiguracji` w `skills/ba-setup/SKILL.md`. Najpierw test kontraktu, potem `SKILL.md`, na końcu `README.md`.

Specyfikacja: [`.ai/specs/2026-11-18-setup-delete-extra-labels.md`](2026-11-18-setup-delete-extra-labels.md)

## Ograniczenia globalne

- Nazwa sekcji: `## Etykiety spoza konfiguracji`. Stoi zaraz po `## Etykiety`.
- Opcje pierwszego pytania: „zostaw wszystkie”, „wybierz”, „skasuj wszystkie”. Rekomendowana stoi pierwsza.
- Opcje drugiego potwierdzenia: „zostaw te”, „skasuj też te”.
- Fraza bez pytania: „nic do skasowania”.
- Polecenie kasowania: `gh label delete --yes -- '<nazwa>'`.
- Zapytanie GraphQL: dokładnie to ze specyfikacji, § Przebieg kroku 7, punkt 2.
- Inne skille nie odwołują się do kroków `ba-setup`. Test `test_no_skill_references_ba_skill_sections` tego pilnuje.

## Na co uważać

- **Numeracja kroków.** Commit przechodzi na krok 8. § Pytania do operatora wymienia krok 8 zamiast 7. Sprawdza Task 2, krok 3.
- **Test na tekst, nie na zachowanie.** Ręczne uruchomienie `ba-setup` jest poza zadaniem. Raport PR-a to mówi.

---

### Task 1: Test kontraktu `ba-setup`

**Pliki:**
- Utwórz: `tests/test_setup_extra_labels.py`

**Interfejsy:**
- Dostarcza: test, który Task 2 i Task 3 robią zielonym.

- [ ] **Krok 1: Test**

```python
"""ba-setup offers to delete repo labels the config does not define."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SETUP_SKILL = REPO_ROOT / "skills/ba-setup/SKILL.md"
README = REPO_ROOT / "README.md"
SECTION = re.compile(
    r"^## Etykiety spoza konfiguracji\n(.*?)(?=^## )", re.MULTILINE | re.DOTALL
)
STEPS = re.compile(r"^## Kroki\n(.*?)(?=^## )", re.MULTILINE | re.DOTALL)


def _text() -> str:
    return SETUP_SKILL.read_text(encoding="utf-8")


def _section() -> str:
    match = SECTION.search(_text())
    assert match, "ba-setup has no '## Etykiety spoza konfiguracji' section"
    return match.group(1)


def test_setup_has_extra_labels_step_before_commit() -> None:
    steps = STEPS.search(_text())
    assert steps, "ba-setup has no '## Kroki' section"
    body = steps.group(1)

    assert re.search(r"^7\. \*\*Etykiety spoza konfiguracji\.\*\*", body, re.MULTILINE)
    assert re.search(r"^8\. \*\*Commit\.\*\*", body, re.MULTILINE)
    assert "§ Etykiety spoza konfiguracji" in body


def test_extra_labels_section_counts_usage_and_deletes() -> None:
    section = _section()

    for phrase in [
        "gh api graphql --paginate",
        "pullRequests(states: [CLOSED, MERGED])",
        "gh label delete --yes -- '<nazwa>'",
        "nic do skasowania",
    ]:
        assert phrase in section, f"missing: {phrase}"


def test_extra_labels_section_asks_with_options_in_order() -> None:
    section = _section()
    first = [section.find(f"„{option}”") for option in
             ["zostaw wszystkie", "wybierz", "skasuj wszystkie"]]
    second = [section.find(f"„{option}”") for option in ["zostaw te", "skasuj też te"]]

    assert -1 not in first and first == sorted(first)
    assert -1 not in second and second == sorted(second)


def test_setup_no_longer_forbids_deleting_every_label() -> None:
    text = _text()

    assert "nie zmieniasz i nie kasujesz" not in text
    assert "Nie zmienia ani nie kasuje istniejących etykiet" not in text
    assert "Nie kasuje etykiet z konfiguracji ani bez zgody operatora" in text


def test_setup_report_lists_deleted_and_kept_labels() -> None:
    assert "etykiety spoza konfiguracji skasowane i zostawione" in _text()


def test_readme_mentions_label_deletion() -> None:
    row = next(
        line for line in README.read_text(encoding="utf-8").splitlines()
        if line.startswith("| [`ba-setup`]")
    )

    assert "etykiety spoza konfiguracji" in row
```

- [ ] **Krok 2: Uruchom test**

Uruchom: `uv run pytest -p no:cacheprovider tests/test_setup_extra_labels.py`
Oczekiwany wynik: FAIL w 6 testach. Brak sekcji, kroku, frazy w raporcie i w `README.md`.

- [ ] **Krok 3: Commit**

```bash
git add tests/test_setup_extra_labels.py
git commit -m "test(ba-setup): kontrakt kroku etykiet spoza konfiguracji (#5)"
```

### Task 2: Krok 7 w `skills/ba-setup/SKILL.md`

Skill: `superpowers:writing-skills`.

**Pliki:**
- Zmień: `skills/ba-setup/SKILL.md:3` (frontmatter `description`)
- Zmień: `skills/ba-setup/SKILL.md:8,16` (wstęp i § Wywołanie)
- Zmień: `skills/ba-setup/SKILL.md:56-74` (§ Kroki i raport)
- Zmień: `skills/ba-setup/SKILL.md:117` (§ Etykiety, reguła)
- Utwórz sekcję po `skills/ba-setup/SKILL.md:118`
- Zmień: `skills/ba-setup/SKILL.md:128,135`

**Interfejsy:**
- Wymaga: test z Task 1.

- [ ] **Krok 1: Frontmatter, wstęp, § Wywołanie.** Dopisz kasowanie etykiet spoza konfiguracji po zgodzie operatora. W `description` zamień „creates missing labels with description and color after consent” na „creates missing labels with description and color after consent, offers to delete repo labels outside the config after consent”.

- [ ] **Krok 2: § Kroki.** Po kroku 6 wstaw:

```markdown
7. **Etykiety spoza konfiguracji.** Proponujesz skasowanie etykiet repo spoza konfiguracji według § Etykiety spoza konfiguracji.
```

Commit dostaje numer 8. Raport dostaje punkt „etykiety spoza konfiguracji skasowane i zostawione”. Zdanie „Do commita dodajesz tylko pliki zapisane w kroku 5.” zostaje.

- [ ] **Krok 3: Reguły.** § Etykiety, linia 117: „Istniejącej etykiety nie zmieniasz. Różny opis albo kolor tylko wypisujesz. Kasowanie etykiet opisuje § Etykiety spoza konfiguracji.” § Pytania do operatora: „Skill kończy turę pytaniem w krokach 3, 5 i 8. W kroku 1 tylko przy istniejących plikach, w kroku 6 tylko przy etykietach do założenia, w kroku 7 tylko przy etykietach spoza konfiguracji.” § Czego nie robi: „Nie zmienia istniejących etykiet. Nie kasuje etykiet z konfiguracji ani bez zgody operatora.”

- [ ] **Krok 4: Sekcja `## Etykiety spoza konfiguracji`.** Treść według specyfikacji, § Przebieg kroku 7 i § Reguły kroku 7. Zapytanie GraphQL i polecenie `gh label delete` w blokach `bash`.

- [ ] **Krok 5: Uruchom test**

Uruchom: `uv run pytest -p no:cacheprovider tests/test_setup_extra_labels.py`
Oczekiwany wynik: PASS 5 testów, FAIL `test_readme_mentions_label_deletion`.

- [ ] **Krok 6: Commit**

```bash
git add skills/ba-setup/SKILL.md
git commit -m "feat(ba-setup): pyta o skasowanie etykiet spoza konfiguracji (#5)"
```

### Task 3: `README.md` i bramka

**Pliki:**
- Zmień: `README.md` (wiersz `ba-setup` w § Skille)

- [ ] **Krok 1: Kod.** Wiersz: `| [\`ba-setup\`](skills/ba-setup/SKILL.md) | Zakłada \`.ai/config/\` i opis procesu dla nowego repozytorium. Po zgodzie kasuje etykiety spoza konfiguracji. |`

- [ ] **Krok 2: Uruchom bramkę**

Uruchom: `uv sync --locked && uv run ruff check tests/ && uv run ruff format --check tests/ && uv run pytest`
Oczekiwany wynik: PASS.

- [ ] **Krok 3: Mutacja.** Skill `ba-mutation-check` dla `tests/test_setup_extra_labels.py`. Cofnij zmianę `SKILL.md` i `README.md`, test pada.

- [ ] **Krok 4: Commit**

```bash
git add README.md
git commit -m "docs(readme): ba-setup kasuje etykiety spoza konfiguracji (#5)"
```
