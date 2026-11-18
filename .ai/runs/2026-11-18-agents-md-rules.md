# Dziennik: plik AGENTS.md z regułami pracy agenta

Issue: #9
Plan: [`.ai/specs/2026-11-18-agents-md-rules-plan.md`](../specs/2026-11-18-agents-md-rules-plan.md)

## Wybory

- Task 1 robi agent `python-developer:developer`. Task 2 i 3 wykonuję sam w głównej sesji.
  - Powód: Task 2 i 3 to gotowa treść z planu, bez decyzji. Podagent przepisałby ją bez zmian.
  - Recenzja całej gałęzi idzie do osobnego agenta.
- `.ai/config/code-review.md:10` miał to samo zdanie „Repo nie ma pliku z regułami pracy agenta”. Issue go nie wymienia. Poprawione, bo po zmianie byłoby fałszywe. Test sprawdza też ten plik. Specyfikacja uzupełniona.
- Zastępnik „§ X” w specyfikacji łamał test odwołań. Zdanie w specyfikacji przepisane bez zastępnika.
- Brak tożsamości gita w worktree. Commity mają autora z historii repo przez `git -c user.name/user.email`, bez zmiany konfiguracji.

## Postęp

- Task 1: `tests/test_agents_md.py`, 7 czerwonych bez `AGENTS.md`. Commit 3296b8f. Kod: agent `python-developer:developer`, sprawdzony przeze mnie.
- Task 2: `AGENTS.md` i `CLAUDE.md` z treści planu. 6 zielonych, 1 czerwony zgodnie z planem. Commit 074e880.
- Task 3: `project.md` i `sdlc.md` wskazują `AGENTS.md`. Commit 164e7a6.
- Bramka jakości zielona: ruff czysty, 98 testów.
- Mutacja testu: 5 mutacji, każda daje czerwień właściwego testu.
  - stare zdanie w `code-review.md`, nagłówek `## Katalog AI`, brak `@AGENTS.md` w `CLAUDE.md`, `uv run` w § Bramka jakości, wiersz CI bez ścieżki.
- Druga droga: skrypt sprawdził każdą ścieżkę i link w `AGENTS.md` i każdą sekcję `project.md`, do której odsyła. Brakują tylko celowo nieistniejące: `.ai/lessons/`, `docs/reviews/`, `docs/superpowers/`.
