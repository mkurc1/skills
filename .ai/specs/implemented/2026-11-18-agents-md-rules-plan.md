# Plik AGENTS.md z regułami pracy agenta — plan implementacji

Issue: #9

**Cel:** Repo ma `AGENTS.md` z regułami pracy agenta i `CLAUDE.md`, który go importuje. Odwołanie „`AGENTS.md` § Katalog `.ai/`” z `ba-ship-pr` trafia w istniejącą sekcję.

**Architektura:** Najpierw test `tests/test_agents_md.py`, który pada. Potem `AGENTS.md` i `CLAUDE.md` w katalogu głównym. Na końcu dwa zdania w `.ai/config/project.md` i `.ai/docs/sdlc.md`.

Specyfikacja: [`.ai/specs/2026-11-18-agents-md-rules.md`](2026-11-18-agents-md-rules.md)

## Ograniczenia globalne

- Nagłówki `AGENTS.md`: `## Rodzaj zmiany`, `## Reguły skilli`, `## Katalog .ai/`, `## Bramka jakości`, `## Proces`.
- `AGENTS.md` nie zawiera komend bramki (`uv run`).
- Bez zmian w `skills/`.
- Commity bez sygnatury agenta.

## Na co uważać

- **Odwołanie z backtickami.** `ba-ship-pr` pisze „`AGENTS.md` § Katalog `.ai/`”. Nagłówek nie ma backticków. Test zdejmuje backticki przed porównaniem. Task 1 sprawdza, że regex łapie co najmniej 2 odwołania.
- **Pliki nieśledzone.** `tracked_files` widzi tylko pliki w gicie. `AGENTS.md` test czyta wprost ze ścieżki, nie przez `tracked_files`.

---

### Task 1: Test `tests/test_agents_md.py`

**Pliki:**
- Utwórz: `tests/test_agents_md.py`

**Interfejsy:**
- Dostarcza: test, który Task 2 i 3 zmieniają na zielony.

- [ ] **Krok 1: Test** — kod wykonawca (agent `python-developer:developer`) pisze według listy:
  - `test_agents_md_has_required_sections`: nagłówki `## ` zawierają `Rodzaj zmiany`, `Reguły skilli`, `Katalog .ai/`, `Bramka jakości`.
  - `test_change_table_covers_every_kind`: tabela w `## Rodzaj zmiany` ma nagłówek `| Rodzaj zmiany | Co przeczytać | Kluczowe reguły |`. Pierwsze kolumny wierszy zawierają kolejno `skills/*/SKILL.md`, `skills/ba-setup/references/`, `tests/`, `.github/workflows/`, `README.md`.
  - `test_ai_directory_section_lists_directories`: `## Katalog .ai/` zawiera `` `config/` ``, `` `docs/` ``, `` `specs/` ``, `` `runs/` ``.
  - `test_quality_gate_points_to_project_md`: `## Bramka jakości` zawiera `.ai/config/project.md` i nie zawiera `uv run`.
  - `test_agents_md_references_resolve`: regex `` `AGENTS\.md` § ([^)”\n]+)[)”] `` na plikach z `tracked_files(REPO_ROOT)` z końcówką `.md`. Co najmniej 2 trafienia. Każda nazwa po zdjęciu backticków i spacji na końcach jest nagłówkiem `## ` w `AGENTS.md`.
  - `test_claude_md_imports_agents_md`: `CLAUDE.md` ma linię równą `@AGENTS.md`.
  - `test_config_no_longer_denies_agents_md`: `.ai/config/project.md` i `.ai/docs/sdlc.md` nie zawierają „Repo nie ma pliku z regułami pracy agenta”.
  - Pomocnik `_section(name)`: treść od `## {name}` do następnego `## ` albo końca pliku.

- [ ] **Krok 2: Uruchom test**

Uruchom: `uv run pytest -p no:cacheprovider tests/test_agents_md.py`
Oczekiwany wynik: FAIL. Brak `AGENTS.md` i `CLAUDE.md`, zdanie wciąż stoi w `project.md`.

- [ ] **Krok 3: Lint**

Uruchom: `uv run ruff check tests/ && uv run ruff format --check tests/`
Oczekiwany wynik: PASS.

- [ ] **Krok 4: Commit**

```bash
git add tests/test_agents_md.py
git commit -m "test(agents): test sekcji AGENTS.md i odwołań do nich (#9)"
```

### Task 2: `AGENTS.md` i `CLAUDE.md`

**Pliki:**
- Utwórz: `AGENTS.md`
- Utwórz: `CLAUDE.md`

**Interfejsy:**
- Wymaga: test z Task 1.
- Dostarcza: sekcję `## Katalog .ai/` dla `ba-ship-pr`.

- [ ] **Krok 1: Kod** — `AGENTS.md`:

````markdown
# Reguły pracy agenta

Ten plik podaje agentowi reguły pracy w tym repozytorium. Czyta go agent, który zmienia skille, szablony, testy, CI albo dokumentację.

Repo jest źródłem skilli `ba-*`. Wynik pracy to dokumenty markdown w `skills/`, testy kontraktów w Pythonie i workflow CI. Repo nie ma kodu aplikacji.

Test `tests/test_agents_md.py` czyta nagłówki `## ` tego pliku. Zmiana nagłówka wymaga zmiany testu i odwołań w `skills/`.

## Rodzaj zmiany

| Rodzaj zmiany | Co przeczytać | Kluczowe reguły |
|---|---|---|
| Treść skilla (`skills/*/SKILL.md`) | § Reguły skilli, `SKILL.md` skilla wołającego i wołanego, test skilla w `tests/` | Skill woła inny skill tylko przez jego `## Wywołanie`. Wartości projektu stoją w `.ai/config/`, nie w skillu. Treść piszesz ze skillem `superpowers:writing-skills`. |
| Szablony `ba-setup` (`skills/ba-setup/references/`) | `skills/ba-setup/SKILL.md`, `skills/ba-setup/references/interview.md`, `tests/test_skill_portability.py` | Szablon to kontrakt `.ai/config/`. Zmiana szablonu albo jego nagłówka `## ` to decyzja opiekuna z `.ai/config/project.md` § Decyzje opiekuna. Znacznik wariantu ma parę w `interview.md`. |
| Testy w `tests/` | `tests/support/tracked_files.py`, `pyproject.toml` | Test czyta pliki śledzone przez git przez `tracked_files`. Nowy test regresyjny sprawdzasz skillem `ba-mutation-check`. Kod testów pisze agent `python-developer:developer`. |
| CI w `.github/workflows/` | `.github/workflows/ci.yml`, `.ai/config/project.md` § Bramka jakości | Joby `lint` i `test` uruchamiają komendy bramki jakości. Zmiana jednej strony wymaga zmiany drugiej. Job `install` liczy skille. |
| Dokumentacja i diagramy (`README.md`, `docs/diagrams/`) | `README.md`, `docs/diagrams/README.md`, `tests/test_readme_diagrams.py` | Nowy albo zmieniony skill aktualizuje tabelę skilli w `README.md` w tym samym PR-ze. Diagram ma źródło `.mmd` i obraz `.png`. Oba commitujesz razem. |

Nowy skill zmienia liczbę skilli w dwóch miejscach: w jobie `install` w `ci.yml` i w `tests/test_skill_frontmatter.py`.

## Reguły skilli

Testy w `tests/` pilnują tych reguł. Złamana reguła daje czerwoną bramkę jakości.

- Każdy skill `ba-*` ma sekcję `## Wywołanie`.
  - Test: `tests/test_skill_contracts.py`.
- Skill woła inny skill tylko przez jego `## Wywołanie`. Nie odsyła do sekcji ani kroku innego skilla.
  - Test: `tests/test_skill_contracts.py`.
- Front matter `SKILL.md` parsuje się jako YAML.
  - Test: `tests/test_skill_frontmatter.py`.
- Skill przenośny nie nazywa projektu, w którym powstał. Wartości projektu stoją w `.ai/config/`.
  - Test: `tests/test_skill_portability.py`.
- Skill nie kopiuje komend bramki jakości. Komendy stoją w `.ai/config/project.md`.
  - Test: `tests/test_skill_portability.py`.
- Plik z sekcji `## Konfiguracja` skilla ma szablon w `skills/ba-setup/references/config/`.
  - Test: `tests/test_skill_portability.py`.
- Sekcja `project.md`, którą skill czyta po nazwie, istnieje w szablonie `project.md`.
  - Test: `tests/test_skill_portability.py`.
- Skill bez pliku konfiguracji odsyła do skilla `ba-setup`.
  - Test: `tests/test_skill_portability.py`.

Jednej reguły test nie pilnuje:

- Zmiana kontraktu zmienia wszystkich czytelników w tym samym PR-ze.
  - Kontrakt to nagłówek albo format, który czyta inny skill albo test.
  - Przed zmianą wyszukaj nagłówek w `skills/`, `tests/` i `.ai/`.

## Katalog .ai/

Katalog `.ai/` trzyma wiedzę o projekcie i przebiegi pracy. Commit zabiera te pliki razem z kodem.

| Katalog | Co leży | Kto pisze |
|---|---|---|
| `config/` | Fakty o projekcie dla skilli: etykiety, stany, szablony, bramka jakości. | `ba-setup`, potem opiekun repo |
| `docs/` | Opis procesu dostarczania zmian w `sdlc.md`. | `ba-setup`, potem opiekun repo |
| `specs/` | Specyfikacje i plany przed kodem. Zrobione leżą w `specs/implemented/`. | `ba-plan`. Przenosi je `ba-ship-pr`. |
| `runs/` | Dzienniki przebiegów autonomicznych: wybory i postęp. | `ba-implement`. Domyka je `ba-ship-pr`. |

Specyfikacje z `docs/superpowers/` przechodzą do `.ai/specs/`. Katalogi `docs/superpowers/` i `docs/reviews/` nie trafiają do repo.

Repo nie prowadzi jeszcze lekcji. Pierwsza lekcja zakłada `.ai/lessons/` i indeks `.ai/lessons.md`.

## Bramka jakości

Komendy bramki stoją w [`.ai/config/project.md` § Bramka jakości](.ai/config/project.md#bramka-jakości). Ten plik ich nie kopiuje.

Zadanie jest gotowe dopiero po zielonej bramce.

## Proces

Drogę zadania od issue do merge'a opisuje [`.ai/docs/sdlc.md`](.ai/docs/sdlc.md).

- Skille do sytuacji w issue: `.ai/config/project.md` § Dobór skilli.
- Decyzje, których agent nie podejmuje sam: `.ai/config/project.md` § Decyzje opiekuna.
- Gałąź, commit i push: reguły gita z sesji agenta.
````

- [ ] **Krok 2: Kod** — `CLAUDE.md`:

```markdown
# Instrukcje dla Claude Code

Reguły pracy agenta stoją w `AGENTS.md`. Ten plik ich nie powtarza.

@AGENTS.md
```

- [ ] **Krok 3: Uruchom test**

Uruchom: `uv run pytest -p no:cacheprovider tests/test_agents_md.py`
Oczekiwany wynik: FAIL tylko w `test_config_no_longer_denies_agents_md`.

- [ ] **Krok 4: Commit**

```bash
git add AGENTS.md CLAUDE.md
git commit -m "docs(agents): AGENTS.md z regułami pracy agenta i CLAUDE.md (#9)"
```

### Task 3: Odwołania w `project.md` i `sdlc.md`

**Pliki:**
- Zmień: `.ai/config/project.md:86`
- Zmień: `.ai/docs/sdlc.md:6`

**Interfejsy:**
- Wymaga: `AGENTS.md` z Task 2.

- [ ] **Krok 1: Kod**
  - `.ai/config/project.md:86` na: „Reguły pracy agenta stoją w `AGENTS.md`. Reguły procesu stoją w `.ai/docs/sdlc.md`.”
  - `.ai/docs/sdlc.md:6` na: „- Reguły pracy agenta stoją w [`AGENTS.md`](../../AGENTS.md). Ten plik ich nie powtarza.”

- [ ] **Krok 2: Uruchom test**

Uruchom: `uv run pytest -p no:cacheprovider tests/test_agents_md.py`
Oczekiwany wynik: PASS.

- [ ] **Krok 3: Bramka jakości**

Uruchom komendy z `.ai/config/project.md` § Bramka jakości.
Oczekiwany wynik: PASS.

- [ ] **Krok 4: Commit**

```bash
git add .ai/config/project.md .ai/docs/sdlc.md
git commit -m "docs(config): project.md i sdlc.md wskazują AGENTS.md (#9)"
```
