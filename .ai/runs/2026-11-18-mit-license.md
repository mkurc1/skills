# Dziennik: licencja MIT dla repozytorium

Issue: #10

Plan: [`.ai/specs/implemented/2026-11-18-mit-license-plan.md`](../specs/implemented/2026-11-18-mit-license-plan.md)

## Postęp

- [x] Task 1: Licencja MIT. Test padał 3/3 przed zmianą, przechodzi 3/3 po zmianie.

## Wybory

- **Wykonanie bez podagenta.** Plan ma 1 zadanie z gotowym kodem 4 plików. Podagent nie dodaje wartości. Recenzję gałęzi robi `ba-ship-pr`.
- **Agent `python-developer:developer` pominięty.** Test leży gotowy w planie. Zgodność z `ruff` sprawdza bramka.

## Weryfikacja

- Bramka jakości: `uv sync --locked`, `ruff check`, `ruff format --check`, `pytest`. Wynik: 94 passed, `uv.lock` bez zmian.
- Druga droga: `gh api licenses/mit --jq .body` z podstawionym rokiem i nazwiskiem. `diff` z `LICENSE` pokazuje tylko końcową pustą linię z wyjścia `gh`.
- Weryfikacja mutacyjna, ręcznie (1 mutacja = 1 czerwony test):
  - bez `LICENSE`: pada `test_license_file_has_mit_text_and_copyright`;
  - bez `license = "MIT"`: pada `test_pyproject_declares_mit`;
  - sekcja bez linku: pada `test_readme_has_license_section_linking_the_file`.

## Po merge

- `gh api repos/mkurc1/skills --jq .license.spdx_id` ma zwrócić `MIT`.

## Wysyłka

- ba-ship-pr: bramka zielona, lokalne review (security, quality, docs) bez znalezisk powyżej LOW w rundzie 1.
- LOW, świadomie pominięte: `tests/test_license.py` sprawdza 3 wiersze `LICENSE`, nie cały tekst. Pełny tekst sprawdził `diff` z `gh api licenses/mit`.
- Specyfikacja i plan przeniesione do `.ai/specs/implemented/`.
