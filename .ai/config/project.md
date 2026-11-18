# Konfiguracja projektu

Ten plik podaje skillom i ludziom stałe fakty o projekcie: repozytorium, język, nazwę gałęzi i bramkę jakości. Czytają go skille `ba-*` oraz proces opisany w `.ai/docs/sdlc.md`.

Skille czytają sekcje po nazwie. Nie zmieniaj nagłówków `## ` i nie usuwaj sekcji.

| Sekcja | Cel | Czytają ją |
|---|---|---|
| Repozytorium | Podaje repozytorium projektu ludziom. | `.ai/docs/sdlc.md` |
| Język | Ustala język tytułów i treści issue. | `ba-github-issues`, `ba-refine-issue` |
| Pojęcia | Ustala słownictwo issue i miejsce definicji terminów. | `ba-github-issues`, `ba-refine-issue` |
| Gałąź | Podaje wzór nazwy gałęzi dla issue. | `ba-github-issues`, `ba-implement` |
| Zgłaszanie błędów spoza zakresu | Mówi, czy pytać przed założeniem issue na znaleziony błąd. | `ba-github-issues`, `ba-implement` |
| Bramka jakości | Podaje komendy, które muszą przejść przed końcem zadania. | `ba-implement`, `ba-ship-pr` |
| Pojedynczy test | Podaje polecenie, które uruchamia jeden plik testów. | `ba-mutation-check` |
| Dokumentacja przed pracą | Wymienia dokumenty do przeczytania przed kodem i pytaniami. | `ba-plan`, `ba-refine-issue` |
| Dobór skilli | Przypisuje skille i agentów do sytuacji w issue. | `ba-plan`, `ba-implement` |
| Decyzje opiekuna | Wymienia decyzje, których agent nie podejmuje sam. | `ba-plan`, `ba-implement`, `ba-refine-issue` |
| Pytania do operatora | Ustala formę pytań do człowieka. | `ba-plan`, `ba-implement`, `ba-refine-issue`, `ba-fix-issue`, `ba-auto-fix-issue` |

## Repozytorium

`mkurc1/skills`. To tylko informacja. Polecenia `gh` biorą repozytorium z katalogu roboczego.

## Język

Tytuł i treść issue są po polsku, z pełną diakrytyką.

## Pojęcia

Tytuł i treść issue są bez żargonu. Nazwa z kodu w backtickach jest dozwolona.

Repo nie ma słownika pojęć. Termin, którego nie da się uniknąć, definiujesz jednym zdaniem w treści issue.

## Gałąź

Nazwa gałęzi ma kształt `<typ>/<n>-<slug>`.

- Typ pochodzi z etykiety issue: `feat` daje `feat/`, `bug` daje `fix/`.
- Issue bez etykiety typu (ani `feat`, ani `bug`) dostaje prefiks `chore/`.
- `<n>` to numer issue.
- Slug jest w ASCII, w kebab-case, do 5 słów.

## Zgłaszanie błędów spoza zakresu

Błąd spoza zadania, który ma dowód, dostaje issue bez pytania użytkownika. Numer issue trafia do raportu z zadania.

## Bramka jakości

Komendy uruchamiasz po kolei, z katalogu głównego repozytorium. Każda ma przejść. Te same komendy uruchamia workflow `.github/workflows/ci.yml` w jobach `lint` i `test`.

Zadanie jest gotowe dopiero po zielonej bramce. Auto-fix poprawia tylko formatowanie i błędy lintera.

### Zawsze

```bash
uv sync --locked
uv run ruff check tests/
uv run ruff format --check tests/
uv run pytest
```

Auto-fix:

```bash
uv run ruff format tests/
uv run ruff check --fix tests/
```

## Pojedynczy test

Polecenie uruchamia jeden plik testów, bez progu pokrycia. Czyta je skill `ba-mutation-check`. Polecenie omija pamięć podręczną narzędzia, żeby test widział zmieniony kod.

```bash
uv run pytest -p no:cacheprovider '<plik>'
```

## Dokumentacja przed pracą

Przeczytaj, zanim dotkniesz kodu i zanim zadasz pytanie:

- `README.md`: wymagania, instalacja i lista skilli;
- test z `tests/`, który pilnuje kontraktu zmienianego skilla albo szablonu `ba-setup`;
- specyfikację z `.ai/specs/` i pasujące lekcje, gdy repo je prowadzi.

Reguły pracy agenta stoją w `AGENTS.md`. Reguły procesu stoją w `.ai/docs/sdlc.md`.

## Dobór skilli

Jedno issue może trafić w kilka wierszy naraz.

| Sytuacja w issue | Skill albo agent |
|---|---|
| Kod testów w Pythonie (`tests/`) | agent `python-developer:developer` |
| Treść skilla (`skills/*/SKILL.md`) albo szablon `ba-setup` | `superpowers:writing-skills` |
| Błąd | `superpowers:systematic-debugging`, potem test, który pada |
| Nowy albo zmieniony test regresyjny | `ba-mutation-check` |
| Szerokie rozpoznanie kodu | agent `Explore` |
| Dokumentacja po zmianie | zaktualizuj `README.md` w tym samym zadaniu |
| Wykonanie planu | `superpowers:subagent-driven-development`. Sposób wykonania: podagent na zadanie z recenzją po każdym zadaniu, potem recenzja całej gałęzi. Kończy się przed jego krokiem `finishing-a-development-branch` |
| Specyfikacja z opiekunem | `superpowers:brainstorming` (używa go `ba-plan` w trybie domyślnym) |

Tabela wymienia to, co łatwo pominąć. Pozostałe skille dobierasz według ich opisów.

Pomiń skille, które z założenia pytają użytkownika. Dotyczy to całej pracy bez operatora: `ba-plan --auto`, kroku planu w `ba-plan` w obu trybach i `ba-implement`. Jedyny wyjątek to rozmowa w trybie domyślnym `ba-plan`. Lista: `superpowers:brainstorming`, `superpowers:finishing-a-development-branch`, `superpowers:writing-plans`, `code-review:fix-report`, `code-review:fix-all`.

## Decyzje opiekuna

Zmiana z tej listy zawsze trafia do pytań do operatora, także gdy dokumentacja podpowiada odpowiedź:

- zmiana, która wymaga zapisu decyzji architektonicznej (ADR);
- zmiana granic modułów;
- nowa biblioteka albo usługa zewnętrzna;
- wyraźna zmiana projektu systemu;
- zmiana kontraktu `.ai/config/`, który czytają skille: nagłówki `## ` w szablonach i same szablony `ba-setup`.

## Pytania do operatora

Pytanie do operatora ma opcje do zaznaczenia. Wysyła je mechanizm narzędzia: pytanie z opcjami w Claude Code, karta w cezarze, odpowiednik w Codex.

- Proza wchodzi w grę tylko wtedy, gdy narzędzie nie ma takiego mechanizmu.
- Każda opcja ma krótki opis skutku.
- Opcja rekomendowana stoi pierwsza.
