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

`{właściciel/nazwa repozytorium}`. To tylko informacja. Polecenia `gh` biorą repozytorium z katalogu roboczego.

## Język

Tytuł i treść issue są {język treści issue, na przykład: po polsku, z pełną diakrytyką}. {Skill do pisania tekstu, gdy repo go ma. Usuń zdanie, gdy brak.}

## Pojęcia

Tytuł i treść issue są bez żargonu. {Przykłady słów zakazanych i ich zamienników. Usuń zdanie, gdy brak.} Nazwa z kodu w backtickach jest dozwolona.

Termin, którego nie da się uniknąć, ma wpis w {link do słownika pojęć, na przykład `docs/glossary.md`}.

## Gałąź

Nazwa gałęzi ma kształt `{wzór nazwy gałęzi, domyślnie <typ>/<n>-<slug>}`.

- Typ pochodzi z etykiety issue: `feat` daje `feat/`, `bug` daje `fix/`.
- Issue bez etykiety typu (ani `feat`, ani `bug`) dostaje prefiks `chore/`.
- `<n>` to numer issue.
- Slug jest w ASCII, w kebab-case, do 5 słów.

## Zgłaszanie błędów spoza zakresu

{Czy pytać przed założeniem issue. Domyślnie: Błąd spoza zadania, który ma dowód, dostaje issue bez pytania użytkownika.} Numer issue trafia do raportu z zadania.

## Bramka jakości

Komendy uruchamiasz po kolei, z katalogu głównego repozytorium. Każda ma przejść. {Workflow CI, który uruchamia te same komendy. Usuń zdanie, gdy repo nie ma CI.}

Zadanie jest gotowe dopiero po zielonej bramce. Auto-fix poprawia tylko formatowanie i błędy lintera.

### Zawsze

```bash
{jedna komenda na linię, tyle linii, ile komend sprawdzających kod}
```

Auto-fix:

```bash
{komenda formatowania}
{komenda lintera z automatyczną poprawką}
```

{Bramka dla części repo, na przykład frontendu: podsekcja ``### Gdy zmiana dotyka `<katalog>/` `` z blokiem komend w formie `(cd '<katalog>' && <komenda>)` i akapitem „Auto-fix:” z blokiem komend. Usuń, gdy repo ma jedną bramkę.}

{Narzędzie granic modułów: podsekcja `### Narzędzie granic modułów` z nazwą narzędzia i pliku reguł. Agent nie dopisuje w nim wyjątków. Usuń, gdy repo go nie ma.}

## Pojedynczy test

Polecenie uruchamia jeden plik testów, bez progu pokrycia. Czyta je skill `ba-mutation-check`. Polecenie omija pamięć podręczną narzędzia, żeby test widział zmieniony kod.

```bash
{polecenie jednego pliku testów, z miejscem na ścieżkę <plik>}
```

{Repo z kilkoma stosami: podsekcja `### <stos>` z poleceniem dla każdego z nich.}

## Dokumentacja przed pracą

Przeczytaj, zanim dotkniesz kodu i zanim zadasz pytanie:

- {mapa dokumentacji, na przykład `docs/README.md`, i dokument obszaru, do którego prowadzi};
- {dokument z regułami domeny, gdy zadanie ich dotyka; usuń, gdy brak};
- {słownik pojęć}, gdy issue używa terminu, którego nie znasz z kodu;
- specyfikację z `.ai/specs/` i pasujące lekcje, gdy repo je prowadzi.

{Plik z regułami pracy agenta, na przykład `AGENTS.md`, i jego sekcja o miejscu reguł.}

## Dobór skilli

Jedno issue może trafić w kilka wierszy naraz.

| Sytuacja w issue | Skill albo agent |
|---|---|
| {Kod w języku programowania projektu} | {skill albo agent dla tego języka programowania} |
| Błąd | `superpowers:systematic-debugging`, potem test, który pada |
| Nowy albo zmieniony test regresyjny | `ba-mutation-check` |
| Szerokie rozpoznanie kodu | agent `Explore` |
| Dokumentacja po zmianie | {skill synchronizacji dokumentacji; bez niego: zaktualizuj dokumentację w tym samym zadaniu} |
| Wykonanie planu | `superpowers:subagent-driven-development`. Sposób wykonania: podagent na zadanie z recenzją po każdym zadaniu, potem recenzja całej gałęzi. Kończy się przed jego krokiem `finishing-a-development-branch` |
| Specyfikacja z opiekunem | `superpowers:brainstorming` (używa go `ba-plan` w trybie domyślnym) |

{Inne sytuacje projektu i ich skille, po jednym wierszu tabeli. Usuń, gdy brak.}

Tabela wymienia to, co łatwo pominąć. Pozostałe skille dobierasz według ich opisów.

Pomiń skille, które z założenia pytają użytkownika. Dotyczy to całej pracy bez operatora: `ba-plan --auto`, kroku planu w `ba-plan` w obu trybach i `ba-implement`. Jedyny wyjątek to rozmowa w trybie domyślnym `ba-plan`. Lista: `superpowers:brainstorming`, `superpowers:finishing-a-development-branch`, `superpowers:writing-plans`, `code-review:fix-report`, `code-review:fix-all`.

## Decyzje opiekuna

Zmiana z tej listy zawsze trafia do pytań do operatora, także gdy dokumentacja podpowiada odpowiedź:

- zmiana, która wymaga zapisu decyzji architektonicznej (ADR);
- zmiana granic modułów;
- nowa biblioteka albo usługa zewnętrzna;
- wyraźna zmiana projektu systemu;
- {inne decyzje projektu; usuń, gdy brak}.

## Pytania do operatora

Pytanie do operatora ma opcje do zaznaczenia. Wysyła je mechanizm narzędzia: pytanie z opcjami w Claude Code, karta w cezarze, odpowiednik w Codex.

- Proza wchodzi w grę tylko wtedy, gdy narzędzie nie ma takiego mechanizmu.
- Każda opcja ma krótki opis skutku.
- Opcja rekomendowana stoi pierwsza.
