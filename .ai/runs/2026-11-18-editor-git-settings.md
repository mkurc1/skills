# Dziennik: Wspólne ustawienia edytora i gita w repo

Issue: #11

Plan: [`.ai/specs/2026-11-18-editor-git-settings-plan.md`](../specs/2026-11-18-editor-git-settings-plan.md)

## Postęp

- [x] Task 1: test `tests/test_repo_settings.py`, `0b50537`. Przed zmianą 9 FAIL, 1 PASS (brak CRLF).
- [x] Task 2: `.editorconfig`, `.gitattributes`, `.gitignore`, `0ffdb94`. 10 PASS.

## Wybory

- Plan wykonany w głównej sesji, bez podagenta na zadanie. Powód: plan zawiera pełny kod testu i pełną treść 3 plików. Recenzję całej gałęzi robi lokalne review `ba-ship-pr`.
- Agent `python-developer:developer` nie pisał testu. Powód: kod testu stał w planie w całości. `ruff` go nie zmienił.
- Commity mają autora operatora przez zmienne `GIT_AUTHOR_*`. Powód: worktree nie ma `user.name` w konfiguracji gita.
- `README.md` bez zmian. Powód: README opisuje skille i instalację, nie ustawienia repo.
- `git add --renormalize .` nie zmienił żadnego pliku. Żaden plik nie miał CRLF.

## Weryfikacja

- Bramka jakości: `uv sync --locked`, `ruff check`, `ruff format --check`, `pytest`. 101 PASS.
- Mutacja: usunięte `*.png binary`, `.worktrees/` i `max_line_length = 100`. 3 testy FAIL. Po przywróceniu 10 PASS.
- Mutacja CRLF: w klonie dodany plik `crlf.md` z CRLF. `test_no_tracked_file_has_crlf` FAIL.
- Druga droga: klon z `core.autocrlf=true`. `git ls-files --eol` pokazuje 72 pliki `w/lf`, 4 PNG `w/-text`, 2 puste `w/none`. Zero CRLF.
- `git check-attr`: `README.md` ma `text: auto`, `eol: lf`. PNG ma `text: unset`.
