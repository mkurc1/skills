# Dziennik: katalog roboczy `ba-ship-pr` w `.ai/scratch/`

Issue: #7

Plan: [`.ai/specs/2026-11-18-ship-pr-scratch-gitignore-plan.md`](../specs/2026-11-18-ship-pr-scratch-gitignore-plan.md)

## Postęp

- [x] Task 1: wpis `.ai/scratch/` w `.gitignore`. Commit `5bd16fa`.
- [x] Task 2: `ba-ship-pr` zapisuje do `.ai/scratch/reviews/`. Commit `a1f742f`.
- [x] Task 3: `ba-setup` dopisuje `.ai/scratch/` do `.gitignore`, `README.md`.

## Wybory

- **Zadania wykonane w głównej sesji, bez podagenta na zadanie.** Każde zadanie to kilka linii tekstu w skillu i test. Recenzję całej gałęzi robi pętla review w `ba-ship-pr`.
- **`import re` dopiero w Task 3.** Plan dawał go w Task 1. Ruff zgłosiłby nieużywany import w commicie Task 1.
- **Test `git check-ignore` przez `shutil.which("git")`, `noqa: S603` i `timeout=30`.** Ruff zgłosił `S607` na gołym `"git"`. Wzorzec z `tests/support/tracked_files.py`.
- **Opis `description` w `ba-setup` wspomina `.ai/scratch/`.** Plan tego nie wymieniał. Opis wylicza wszystkie skutki skilla, więc nowy skutek też.
- **Autor commitów z historii repo i konta `gh`.** Środowisko nie ma `user.name`. Ustawione tylko dla polecenia `git -c`.
- **Cofnięty lokalny commit autosave narzędzia.** Commit `cezar autosave (run finalize)` z samą specyfikacją. Nie był wypchnięty. Cofnięty `git reset --soft`, specyfikacja weszła do commita Task 1.

## Weryfikacja

- Bramka jakości: `uv sync --locked`, `ruff check`, `ruff format --check` zielone. `pytest`: **96 passed**.
- Weryfikacja mutacyjna `tests/test_scratch_dir.py`. Każda mutacja wywala 1 test:
  - `.gitignore` bez linii `.ai/scratch/`;
  - `ba-ship-pr` z `mkdir -p .claude/scratch/reviews`;
  - `ba-setup` bez nagłówka `## Wpis w .gitignore`;
  - krok 4 `ba-setup` bez odwołania do § Wpis w .gitignore;
  - `README.md` bez zdania o `.ai/scratch/`.
- Druga droga: blok 1.0 z `ba-ship-pr` w świeżym repo z `mktemp -d`.
  - Bez wpisu `git check-ignore -q .ai/scratch/x` daje kod 1, z wpisem kod 0.
  - Snapshot i indeks powstają w `.ai/scratch/reviews/`.
  - `git add -A` zabiera tylko `.gitignore` i `app.txt`, bez snapshotu.
