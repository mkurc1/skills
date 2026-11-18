# Reguły pracy agenta

Ten plik podaje agentowi reguły pracy w tym repozytorium. Czyta go agent, który zmienia skille, szablony, testy, CI albo dokumentację.

Repo jest źródłem skilli `ba-*`. Wynik pracy to dokumenty markdown w `skills/`, testy kontraktów w Pythonie i workflow CI. Repo nie ma kodu aplikacji.

Test `tests/test_agents_md.py` czyta nagłówki `## ` tego pliku. Zmiana nagłówka wymaga zmiany testu i odwołań w `skills/`.

## Rodzaj zmiany

| Rodzaj zmiany | Co przeczytać | Kluczowe reguły |
|---|---|---|
| Treść skilla (`skills/*/SKILL.md`) | § Reguły skilli, `SKILL.md` skilla wołającego i wołanego, test skilla w `tests/` | Łączenie skilli: `.ai/docs/sdlc.md` § Łączenie skilli. Wartości projektu stoją w `.ai/config/`, nie w skillu. |
| Szablony `ba-setup` (`skills/ba-setup/references/`) | `skills/ba-setup/SKILL.md`, `skills/ba-setup/references/interview.md`, `tests/test_skill_portability.py`, `tests/test_setup_extra_labels.py` | Szablon to kontrakt `.ai/config/`. Zmiana szablonu albo jego nagłówka `## ` to decyzja opiekuna z `.ai/config/project.md` § Decyzje opiekuna. Znacznik wariantu ma parę w `interview.md`. |
| Testy w `tests/` | `tests/support/tracked_files.py`, `pyproject.toml` | Test, który przegląda katalog, bierze pliki z `tracked_files`. |
| CI w `.github/workflows/` | `.github/workflows/ci.yml`, `.ai/config/project.md` § Bramka jakości | Komendy jobów `lint` i `test` opisuje `.ai/config/project.md` § Bramka jakości. Job `install` liczy skille. |
| Dokumentacja i diagramy (`README.md`, `docs/diagrams/`) | `README.md`, `docs/diagrams/README.md`, `tests/test_readme_diagrams.py` | Diagram zmieniasz według `docs/diagrams/README.md`. |

Skille i agentów do każdego rodzaju zmiany podaje `.ai/config/project.md` § Dobór skilli.

Nowy albo usunięty skill: `.ai/config/definition-of-done.md` § Gdy zmiana dotyka `skills/`.

## Reguły skilli

Testy w `tests/` pilnują tych reguł. Złamana reguła daje czerwoną bramkę jakości.

- Każdy skill `ba-*` ma sekcję `## Wywołanie`.
  - Test: `tests/test_skill_contracts.py`.
- Skill nie odsyła do sekcji ani kroku innego skilla.
  - Test: `tests/test_skill_contracts.py`.
- Front matter `SKILL.md` parsuje się jako YAML.
  - Test: `tests/test_skill_frontmatter.py`.
- Skill przenośny nie nazywa projektu, w którym powstał. Wartości projektu stoją w `.ai/config/`.
  - Test: `tests/test_skill_portability.py`.
- Plik z sekcji `## Konfiguracja` skilla ma szablon w `skills/ba-setup/references/config/`.
  - Test: `tests/test_skill_portability.py`.
- Sekcja `project.md`, którą skill czyta po nazwie, istnieje w szablonie `project.md`.
  - Test: `tests/test_skill_portability.py`.
- Skill bez pliku konfiguracji odsyła do skilla `ba-setup`.
  - Test: `tests/test_skill_portability.py`.

Tych reguł test nie pilnuje:

- Łączenie skilli według `.ai/docs/sdlc.md` § Łączenie skilli. Test łapie tylko odwołania do sekcji i kroków.
- Skill nie kopiuje komend bramki jakości. Komendy stoją w `.ai/config/project.md`.
  - `tests/test_skill_portability.py` szuka tylko komend spoza tego repo.
- Zmiana kontraktu zmienia wszystkich czytelników w tym samym PR-ze.
  - Kontrakt to nagłówek albo format, który czyta inny skill albo test.
  - Przed zmianą wyszukaj nagłówek w `skills/`, `tests/` i `.ai/`.

## Katalog .ai/

Katalog `.ai/` trzyma wiedzę o projekcie i przebiegi pracy. Commit zabiera te pliki razem z kodem.

| Katalog | Co leży | Kto pisze |
|---|---|---|
| `config/` | Fakty o projekcie dla skilli: etykiety, stany, szablony, bramka jakości. | `ba-setup`, potem opiekun repo |
| `docs/` | Opis procesu dostarczania zmian w `sdlc.md`. | `ba-setup`, potem opiekun repo |
| `specs/` | Specyfikacje, plany i plany testów przed kodem. Zrobione leżą w `specs/implemented/`. | `ba-plan` i `ba-qa`. Przenosi je `ba-ship-pr`. |
| `runs/` | Dzienniki przebiegów autonomicznych: wybory i postęp. | `ba-implement`. Domyka je `ba-ship-pr`. |

Specyfikacje z `docs/superpowers/` przechodzą do `.ai/specs/`. Katalogi `docs/superpowers/` i `docs/reviews/` nie trafiają do repo.

Repo nie prowadzi jeszcze lekcji. Pierwsza lekcja zakłada `.ai/lessons/` i indeks `.ai/lessons.md`.

## Bramka jakości

Komendy bramki stoją w [`.ai/config/project.md` § Bramka jakości](.ai/config/project.md#bramka-jakości). Ten plik ich nie kopiuje.

## Proces

Drogę zadania od issue do merge'a opisuje [`.ai/docs/sdlc.md`](.ai/docs/sdlc.md).

- Skille do sytuacji w issue: `.ai/config/project.md` § Dobór skilli.
- Decyzje, których agent nie podejmuje sam: `.ai/config/project.md` § Decyzje opiekuna.
- Nazwa gałęzi: `.ai/config/project.md` § Gałąź.
- Commit i push: reguły gita z sesji agenta.
