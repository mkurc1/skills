# Licencja MIT dla repozytorium

Issue: #10

## Cel

Repo `mkurc1/skills` jest publiczne, ale nie ma licencji. Bez licencji nikt nie może legalnie kopiować ani zmieniać skilli. Po zmianie repo ma licencję MIT, a GitHub pokazuje ją na stronie repozytorium.

## Zakres

- Plik `LICENSE` w katalogu głównym z pełnym, kanonicznym tekstem licencji MIT.
- Wiersz praw autorskich: `Copyright (c) 2026 Michał Kurcewicz`.
- Pole `license = "MIT"` w sekcji `[project]` w `pyproject.toml`.
- Sekcja `## Licencja` na końcu `README.md` z odesłaniem do `LICENSE`.
- Test `tests/test_license.py`, który pilnuje trzech punktów wyżej.

### Poza zakresem

- Nagłówki licencji w plikach skilli. Issue je wyklucza.
- `AGENTS.md` i pliki konfiguracji repo. Mają osobne issue.

## Projekt

- **Tekst `LICENSE`.** Kanoniczny tekst MIT z choosealicense.com, bez zmian w słowach. GitHub rozpoznaje licencję biblioteką `licensee`. Ta biblioteka porównuje tekst z wzorcem, więc każda zmiana słów grozi brakiem rozpoznania.
- **Pole w `pyproject.toml`.** Format z PEP 639: wyrażenie SPDX jako napis, `license = "MIT"`. SPDX to standardowy zestaw identyfikatorów licencji. Tabela `license = { text = "MIT" }` to starszy format, odrzucony jako przestarzały.
- **`uv.lock`.** Projekt ma `package = false`. Pole licencji nie wpływa na zależności, więc `uv sync --locked` przechodzi bez zmiany `uv.lock`.
- **Sekcja w `README.md`.** Ostatnia sekcja pliku, po `## Testy`. Jedno zdanie z linkiem `[LICENSE](LICENSE)`.

## Plan

1. Test `tests/test_license.py` pada bez `LICENSE`, pola i sekcji. Sprawdzenie: `uv run pytest tests/test_license.py`.
2. Dodanie `LICENSE`, pola i sekcji. Sprawdzenie: ten sam test przechodzi.
3. Bramka jakości z `project.md`. Sprawdzenie: wszystkie 4 komendy przechodzą.

## Gotowe gdy

- `uv run pytest tests/test_license.py` przechodzi.
- `LICENSE` zaczyna się wierszem `MIT License` i ma wiersz `Copyright (c) 2026 Michał Kurcewicz`.
- `pyproject.toml` ma `license = "MIT"`.
- `README.md` ma sekcję `## Licencja` z linkiem do `LICENSE`.
- Bramka jakości przechodzi.
- Po merge do `main`: `gh api repos/mkurc1/skills --jq .license.spdx_id` zwraca `MIT`.

## Ryzyka i otwarte pytania

- GitHub rozpoznaje licencję dopiero na gałęzi domyślnej. Kryterium „GitHub pokazuje MIT” sprawdzisz po merge.
