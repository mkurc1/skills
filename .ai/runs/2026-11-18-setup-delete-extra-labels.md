# Dziennik: `ba-setup` pyta o skasowanie etykiet spoza konfiguracji

Issue: #5

Plan: [`.ai/specs/2026-11-18-setup-delete-extra-labels-plan.md`](../specs/2026-11-18-setup-delete-extra-labels-plan.md)

## Postęp

- [x] Task 1: test kontraktu, `6a1bf45`. Przed zmianą 6 testów FAIL.
- [x] Task 2: krok 7 w `SKILL.md`, `1a39568`. 5 z 6 testów PASS, `README.md` jeszcze FAIL.
- [x] Task 3: `README.md` i bramka. Bramka zielona: 87 testów PASS, `ruff` czysty.

## Wybory

- Plan wykonany w głównej sesji, zadanie po zadaniu, bez podagenta na zadanie. Powód: 3 małe zmiany tekstu i jeden plik testu. Recenzję całej gałęzi robi świeży podagent i lokalne review `ba-ship-pr`.
- Commity mają autora operatora przez zmienne `GIT_AUTHOR_*`. Powód: worktree nie ma `user.name` w konfiguracji gita. Konfiguracji nie zmieniałem.
- Recenzja całej gałęzi zostaje dla lokalnego review w `ba-ship-pr`.

## Weryfikacja

- Bramka jakości: `uv sync --locked`, `ruff check`, `ruff format --check`, `pytest`. 87 PASS.
- Mutacja: `SKILL.md` i `README.md` cofnięte do `main`. `tests/test_setup_extra_labels.py` daje 6 FAIL. Po przywróceniu 6 PASS.
- Druga droga: zapytanie GraphQL wycięte z `SKILL.md` i uruchomione na `mkurc1/skills`. Zwraca 17 etykiet z liczbami. Spoza konfiguracji wychodzi 9: `accessibility`, `documentation`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix`. Zgodne z § Dowód w issue.
