# Plik AGENTS.md z regułami pracy agenta w repo

Issue: #9

## Cel

Agent, który zmienia to repo, dostaje reguły pracy w jednym pliku `AGENTS.md`. Dziś szuka ich w `README.md`, `.ai/docs/sdlc.md` i testach. `skills/ba-ship-pr/SKILL.md:234` i `:249` odsyłają do sekcji „`AGENTS.md` § Katalog `.ai/`”, której nie ma.

## Zakres

- Nowy `AGENTS.md` w katalogu głównym, po polsku, w stylu `.ai/config/`.
- Nowy `CLAUDE.md` w katalogu głównym z importem `@AGENTS.md`.
- Zdanie „Repo nie ma pliku z regułami pracy agenta” w `.ai/config/project.md` § Dokumentacja przed pracą i w `.ai/docs/sdlc.md` zastąpione odesłaniem do `AGENTS.md`.
- To samo zdanie w `.ai/config/code-review.md:10`. Issue go nie wymienia. Znalezione przy implementacji: po zmianie zdanie byłoby fałszywe.
- Nowy test `tests/test_agents_md.py`.

### Poza zakresem

- Zmiany w skillach i w szablonach `ba-setup` (`skills/ba-setup/references/`). Issue je wyklucza.
- Licencja i pliki konfiguracji repo. Mają osobne issue.
- Katalog `.ai/lessons/`. Repo go jeszcze nie prowadzi. `AGENTS.md` mówi o nim jedno zdanie pod tabelą, bo czytają go `ba-ship-pr` i DoD.

## Odpowiedzi operatora

- **Forma `CLAUDE.md`:** import `@AGENTS.md`.
  - Odrzucone: dowiązanie symboliczne. Psuje się na Windows i w części narzędzi. Kopiuje całą treść zamiast odsyłać.
- **Test:** tak. Test pilnuje sekcji `AGENTS.md` i odwołań do nich.
  - Odrzucone: brak testu. Zmiana nazwy sekcji po cichu zepsułaby odwołanie z `ba-ship-pr`.
- **Reguły:** tabela, sekcja „Katalog `.ai/`” i reguły, których już pilnują testy.
  - Odrzucone: same sekcje z issue. Agent dalej szukałby reguł w testach.

## Projekt

### `AGENTS.md`

Sekcje `## ` w tej kolejności:

1. Wstęp bez nagłówka: 2 zdania o repo. Repo to źródło skilli `ba-*`. Wynikiem są dokumenty markdown, testy w Pythonie i CI.
2. `## Rodzaj zmiany`: tabela z kolumnami „Rodzaj zmiany”, „Co przeczytać”, „Kluczowe reguły”. Wiersze:
   - Treść skilla (`skills/*/SKILL.md`).
   - Szablony `ba-setup` (`skills/ba-setup/references/`).
   - Testy w `tests/`.
   - CI w `.github/workflows/`.
   - Dokumentacja i diagramy (`README.md`, `docs/diagrams/`).
3. `## Reguły skilli`: reguły z testów, każda z nazwą testu, który jej pilnuje.
   - Każdy skill `ba-*` ma sekcję `## Wywołanie`. Skille wołają się tylko przez nią, bez odwołań do sekcji i kroków innego skilla. Test: `tests/test_skill_contracts.py`.
   - Front matter `SKILL.md` parsuje się jako YAML. Repo ma 11 skilli. Test: `tests/test_skill_frontmatter.py`.
   - Skill przenośny nie nazywa projektu. Wartości projektu stoją w `.ai/config/`. Test: `tests/test_skill_portability.py`.
   - Skill nie kopiuje komend bramki jakości. Komendy stoją w `.ai/config/project.md`.
   - Plik konfiguracji, który skill wymienia w sekcji `## Konfiguracja`, ma szablon w `skills/ba-setup/references/config/`.
   - Sekcja `project.md`, którą skill czyta po nazwie, istnieje w szablonie.
   - Zmiana kontraktu zmienia wszystkich czytelników w tym samym PR-ze. Kontrakt to nagłówek albo format, który czyta inny skill albo test.
4. `## Katalog .ai/`: tabela „Katalog → co leży”.
   - `config/`: fakty o projekcie dla skilli. Generuje je `ba-setup`.
   - `docs/`: opis procesu (`sdlc.md`).
   - `specs/`: specyfikacje i plany przed kodem. Zrobione przechodzą do `specs/implemented/`.
   - `runs/`: dzienniki przebiegów autonomicznych.
5. `## Bramka jakości`: odesłanie do `.ai/config/project.md` § Bramka jakości. Bez kopii komend.
6. `## Proces`: odesłanie do `.ai/docs/sdlc.md` i reguł gita z sesji.

Nagłówek sekcji to `## Katalog .ai/`. Odwołanie w `ba-ship-pr` brzmi „`AGENTS.md` § Katalog `.ai/`”. Test porównuje nazwę bez backticków.

### `CLAUDE.md`

```markdown
# Instrukcje dla Claude Code

Reguły pracy agenta stoją w `AGENTS.md`. Ten plik ich nie powtarza.

@AGENTS.md
```

### Zmiany odwołań

- `.ai/config/project.md:86`: „Reguły pracy agenta stoją w `AGENTS.md`. Reguły procesu stoją w `.ai/docs/sdlc.md`.”
- `.ai/docs/sdlc.md:6`: „Reguły pracy agenta stoją w [`AGENTS.md`](../../AGENTS.md). Ten plik ich nie powtarza.”
  - Kształt zdania bierzesz z szablonu `skills/ba-setup/references/sdlc.md:6`.

### Test `tests/test_agents_md.py`

- `AGENTS.md` ma sekcje: `Rodzaj zmiany`, `Reguły skilli`, `Katalog .ai/`, `Bramka jakości`.
- Tabela w `## Rodzaj zmiany` ma 3 kolumny i wiersze dla `skills/*/SKILL.md`, `skills/ba-setup/references/`, `tests/`, `.github/workflows/`, `README.md`.
- `## Katalog .ai/` wymienia `config/`, `docs/`, `specs/`, `runs/`.
- `## Bramka jakości` odsyła do `project.md` i nie zawiera `uv run`.
- Każde odwołanie do sekcji `AGENTS.md` w plikach `.md` śledzonych przez git trafia w istniejący nagłówek `AGENTS.md`.
- `CLAUDE.md` ma linię `@AGENTS.md`.
- `.ai/config/project.md` i `.ai/docs/sdlc.md` nie zawierają zdania „Repo nie ma pliku z regułami pracy agenta”.

## Plan

1. Test `tests/test_agents_md.py` pada bez `AGENTS.md`. Sprawdzenie: `uv run pytest tests/test_agents_md.py`.
2. `AGENTS.md` i `CLAUDE.md`. Sprawdzenie: test zielony poza asercją o zdaniu.
3. Odwołania w `project.md` i `sdlc.md`. Sprawdzenie: test zielony, cała bramka zielona.

## Gotowe gdy

- `uv run pytest tests/test_agents_md.py` przechodzi.
- Bramka jakości z `.ai/config/project.md` przechodzi.
- `grep -rn "Repo nie ma pliku z regułami pracy agenta" .ai/` nic nie zwraca.

## Ryzyka i otwarte pytania

- `ba-setup` w nowym repo pisze `project.md` z szablonu. Szablon dalej mówi o „pliku z regułami pracy agenta, na przykład `AGENTS.md`”. To poprawne. Szablonu nie zmieniamy.
- Wyrażenie regularne odwołania musi złapać oba wiersze `ba-ship-pr` (`:234`, `:249`). Test sprawdza, że znalazł co najmniej 2.
