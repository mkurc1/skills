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
- Recenzja całej gałęzi (osobny agent): 6 drobnych uwag, nic blokującego. Przyjęte 5.
  - Test odwołań wymaga 2 odwołań z `ba-ship-pr`, nie z dowolnego pliku. Same specyfikacje spełniały próg.
  - Test bramki szuka `uv `, nie tylko `uv run`.
  - `specs/` pisze też `ba-qa` (plany testów).
  - Reguła „woła tylko przez `## Wywołanie`” przeszła do reguł bez testu. Test łapie tylko odwołania do sekcji i kroków.
  - Wiersz szablonów `ba-setup` wymienia `tests/test_setup_extra_labels.py`.
  - Odrzucona: szerszy regex odwołań z kropką jako końcem. Uciąłby nazwę „Katalog `.ai/`”.
  - Treść `AGENTS.md` odbiega przez to od bloku w planie. Plan zostaje bez zmian, źródłem jest `AGENTS.md`.
- Bramka po poprawkach zielona: 98 testów.
- Krok dokumentacji: zdanie w `README.md` § Testy z odesłaniem do `AGENTS.md`. Commit 3b202a7.

## ba-ship-pr

- Bramka zielona przed review.
- Runda 1 review (security, quality, docs, potem challenger i cross-verifier).
  - Security: 0 znalezisk.
  - Przyjęte: kopie z `project.md` § Dobór skilli w tabeli `AGENTS.md` zastąpione odesłaniem. Usunięta kopia zdania o zielonej bramce.
  - Przyjęte: reguła o kopii komend bramki przeszła do reguł bez testu. Test szuka tylko komend spoza repo.
  - Przyjęte: § Proces odsyła do `project.md` § Gałąź.
  - Przyjęte: kryterium grep w specyfikacji zawężone do `.ai/config/` i `.ai/docs/`. Opis testu w specyfikacji uzupełniony o `code-review.md` i `uv `. Zakres uzupełniony o `README.md`.
  - Przyjęte: zdanie o `tracked_files` zawężone do testów, które przeglądają katalog.
  - Odrzucone przez challengera: powtórzenie reguły w obrębie jednego pliku, druga asercja `uv ` w teście `AGENTS.md`.
  - Zostają jako LOW: skan odwołań obejmuje archiwum `.ai/specs/`, regex odwołań wymaga backticków.
- Issue spoza zakresu: #14 (test kopii komend bramki nie zna komend repo), #15 (`ba-ship-pr` odsyła do sekcji `AGENTS.md`, której nie ma w innych repo).
- Runda 2 review (quality, docs). Security pominięty: poprawki to sam tekst, runda 1 dała 0.
  - Przyjęte (MEDIUM): reguła o `## Wywołanie` w `AGENTS.md` kopiowała `sdlc.md` § Łączenie skilli. Zastąpiona odesłaniem.
  - Przyjęte (MEDIUM): liczba skilli w `AGENTS.md` kopiowała DoD i rozjeżdżała się z nim. `AGENTS.md` odsyła do DoD. DoD dostał brakujący `tests/test_skill_frontmatter.py`.
  - Przyjęte (LOW): specyfikacja opisuje regułę łączenia skilli jako regułę bez testu.
