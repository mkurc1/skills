# Pull requesty

Ten plik podaje fakty o PR-ach w tym repozytorium. Czytają go skille `ba-ship-pr` i `ba-wait-checks`. Kroki stoją w skillach, fakty tutaj.

Etykiety plik wskazuje nazwą logiczną. Prawdziwą nazwę podaje [`labels.md`](labels.md).

## Gałąź główna

Gałąź główna to `{gałąź domyślna repo}`. PR idzie zawsze do niej.

- Ruleset gałęzi głównej nazywa się `{nazwa rulesetu; usuń punkt, gdy repo go nie ma}`.
- {Link do opisu ochrony gałęzi głównej. Usuń punkt, gdy brak.}

## Opis PR-a

Opis ma sekcje szablonu {plik szablonu opisu, na przykład `.github/pull_request_template.md`}: {lista sekcji `## …`}.

- Żadna sekcja nie jest pusta.
- {Komenda lokalnego sprawdzenia opisu w bloku bash. Usuń punkt, gdy repo jej nie ma.}
- Wystawiasz PR {gotowy do review albo jako draft}.

## Dowód weryfikacji

{Ścieżki, których zmiana wymaga dowodu w opisie PR-a, na przykład rdzeń domeny. Usuń akapit, gdy dowód nie jest wymagany.}

- Dowód to wynik weryfikacji mutacyjnej albo niezależne sprawdzenie drugą drogą.
- Brak wymaganego dowodu to uwaga blokująca w review.

## Werdykt review AI

<!-- ba-setup: wariant review-ai -->
{Gdzie review AI w CI zapisuje werdykt: autor komentarza, kształt bloku werdyktu i komenda `gh`, która go pobiera. Do tego: który werdykt daje zielony check i kiedy PR dostaje etykietę zablokowanego PR-a.}
<!-- ba-setup: koniec wariantu -->
<!-- ba-setup: wariant bez-review-ai -->
Repo nie ma review AI w CI. Werdykt daje człowiek w review PR-a.
<!-- ba-setup: koniec wariantu -->

## Merge

<!-- ba-setup: wariant merge-automatyczny -->
GitHub merguje PR sam (auto-merge) po zielonych checkach{dopisek o review według pytania 10 wywiadu albo nic}. Etykieta wstrzymanego merge'a go zatrzymuje.

{Link do opisu auto-merge'a w dokumentacji repo. Usuń, gdy brak.}
<!-- ba-setup: koniec wariantu -->
<!-- ba-setup: wariant merge-przez-człowieka -->
Człowiek merguje PR po zielonych checkach{dopisek o review według pytania 10 wywiadu albo nic}. Etykieta wstrzymanego merge'a mówi mu, że PR jeszcze nie jest gotowy.
<!-- ba-setup: koniec wariantu -->

## Obszary wrażliwe

Błędna poprawka w tych ścieżkach zmienia wynik systemu, dane albo zachowanie agenta.

| Obszar | Ścieżki |
|---|---|
| {Obszar z wywiadu, na przykład migracje bazy} | {ścieżki} |
| Konfiguracja agenta i CI | `.ai/config/`, `.agents/skills/`, `.github/workflows/` |

Kierunek poprawki wybierasz według tych źródeł: {dokumenty z regułami domeny} i sąsiedni kod.

## Pliki blokad zależności

Plik blokady trzyma dokładne wersje pakietów. Powstaje z manifestu: {pliki manifestów w repo}.

| Plik | Regeneracja przy konflikcie | Podbicie jednego pakietu |
|---|---|---|
| {plik blokady} | {wersja z gałęzi głównej, potem regeneracja, na przykład `git checkout --theirs '<plik>' && (cd '<katalog>' && npm install --package-lock-only)`} | {komenda podbicia jednego pakietu} |

### Sprawdzenie diffu pliku blokady po podbiciu

Ponowne wygenerowanie pliku blokady potrafi zmienić wpisy innych pakietów.

- Policz pakiety, którym zmienia się wersja. Podbicie jednego pakietu ma zmienić jedną wersję.
- Inny pakiet traci tylko wpisy plików dla wybranych platform? Sprawdź, czy te platformy w ogóle instaluje.
- Wynik opisz w PR-ze, zamiast twierdzić „jedna zależność”.

## Checki w CI

Główny workflow CI to `{plik workflowu CI}`.

Wymagane checki przed merge:

- {nazwa wymaganego checku, po jednym punkcie: z rulesetu gałęzi głównej albo z ochrony gałęzi}

{Skan zależności w CI i czy blokuje merge. Usuń zdanie, gdy CI go nie ma.}
