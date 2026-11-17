# Pull requesty

Ten plik podaje fakty o PR-ach w tym repozytorium. Czytają go skille `ba-ship-pr` i `ba-wait-checks`. Kroki stoją w skillach, fakty tutaj.

Etykiety plik wskazuje nazwą logiczną. Prawdziwą nazwę podaje [`labels.md`](labels.md).

## Gałąź główna

Gałąź główna to `main`. PR idzie zawsze do niej.

- Gałąź `main` nie ma rulesetu ani ochrony gałęzi.

## Opis PR-a

Repo nie ma pliku szablonu opisu. Opis ma sekcje: `## Dlaczego`, `## Co się zmienia`, `## Weryfikacja`.

- Żadna sekcja nie jest pusta.
- Wystawiasz PR gotowy do review.

## Dowód weryfikacji

- Dowód to wynik weryfikacji mutacyjnej albo niezależne sprawdzenie drugą drogą.
- Brak wymaganego dowodu to uwaga blokująca w review.

## Werdykt review AI

Repo nie ma review AI w CI. Werdykt daje człowiek w review PR-a.

## Merge

Człowiek merguje PR po zielonych checkach. Etykieta wstrzymanego merge'a mówi mu, że PR jeszcze nie jest gotowy.

## Obszary wrażliwe

Błędna poprawka w tych ścieżkach zmienia wynik systemu, dane albo zachowanie agenta.

| Obszar | Ścieżki |
|---|---|
| Konfiguracja agenta i CI | `.ai/config/`, `.agents/skills/`, `.github/workflows/` |

Kierunek poprawki wybierasz według tych źródeł: `README.md`, testy w `tests/` i sąsiedni kod.

## Pliki blokad zależności

Plik blokady trzyma dokładne wersje pakietów. Powstaje z manifestu: `pyproject.toml`.

| Plik | Regeneracja przy konflikcie | Podbicie jednego pakietu |
|---|---|---|
| `uv.lock` | `git checkout --theirs 'uv.lock' && uv lock` | `uv lock --upgrade-package '<pakiet>'` |

### Sprawdzenie diffu pliku blokady po podbiciu

Ponowne wygenerowanie pliku blokady potrafi zmienić wpisy innych pakietów.

- Policz pakiety, którym zmienia się wersja. Podbicie jednego pakietu ma zmienić jedną wersję.
- Inny pakiet traci tylko wpisy plików dla wybranych platform? Sprawdź, czy te platformy w ogóle instaluje.
- Wynik opisz w PR-ze, zamiast twierdzić „jedna zależność”.

## Checki w CI

Główny workflow CI to `.github/workflows/ci.yml`.

Wymagane checki przed merge: brak. Gałąź `main` nie ma rulesetu ani ochrony gałęzi.

CI uruchamia joby `lint`, `test` i `install`. Człowiek merguje PR dopiero po zielonym wyniku każdego z nich.
