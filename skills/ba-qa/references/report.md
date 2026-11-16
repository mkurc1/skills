# Szablon raportu

Raport `YYYY-MM-DD-slug-qa-report.md` leży obok specyfikacji i planu testów. Kolejne przejście nadpisuje plik.

Pierwsza linia raportu to werdykt przejścia. Dokładnie jedna z trzech:

- `Werdykt: PASS`: każdy scenariusz ma PASS.
- `Werdykt: FAIL`: co najmniej 1 FAIL.
- `Werdykt: BLOCKED`: brak FAIL i co najmniej 1 BLOCKED, albo plan bez scenariuszy.

````markdown
Werdykt: {PASS albo FAIL albo BLOCKED}

# {Tytuł} — raport QA

Dotyczy issue #{n}.

Plan testów: [`{YYYY-MM-DD-slug}-qa.md`]({YYYY-MM-DD-slug}-qa.md)

## Pokrycie

- Sprawdzone (PASS albo FAIL): {liczba} z {liczba wszystkich}
- Niezweryfikowane (BLOCKED): {liczba}, powody: {lista powodów}

## Scenariusze

| Scenariusz | Werdykt | Zrzut | Uwagi |
|---|---|---|---|
| S{k}: {nazwa} | {PASS, FAIL albo BLOCKED} | `{ścieżka zrzutu albo — przy BLOCKED bez wykonania scenariusza}` | {jedno zdanie} |

## FAIL

### S{k}: {nazwa}

- **Kroki:** {numerowana lista kroków}
- **Oczekiwanie:** {co mówi specyfikacja} — `{ścieżka specyfikacji:linia}`
- **Wynik:** {co zrobiła aplikacja}
- **Drugie sprawdzenie:** {wynik od świeżej strony; adnotacja „wynik niestabilny”, gdy różni się od pierwszego}

## BLOCKED

### S{k}: {nazwa}

- **Powód:** {brak środowiska, brak informacji w specyfikacji, nierozstrzygnięta uwaga z recenzji planu albo działanie zakazane}
- **Czego brakuje:** {konkretnie: usługa, narzędzie albo zdanie specyfikacji}

## Recenzja planu

- **Recenzent:** {podagent albo skill sam}
- **Rundy:** {liczba}
- **Uwagi bez poprawki:** {lista albo „brak”}

## Sprzątanie

- **Usunięte:** {lista danych i sposób usunięcia}
- **Nie udało się usunąć:** {lista albo „brak”}

## Propozycje E2E

{Scenariusze warte stałego testu, po jednej linii, z katalogiem testów. Przy FAIL albo BLOCKED: „Brak, issue E2E powstaje dopiero przy werdykcie PASS.” Pusta propozycja przy PASS: „Brak, bo {test albo issue} pokrywa te przypadki.”}
````

Zasady:

- Sekcje „FAIL” i „BLOCKED” bez wpisów zawierają słowo „brak”.
- Każdy scenariusz z `Zapisuje dane: tak` ma wpis w sekcji „Sprzątanie”.
- Zrzuty leżą poza commitem. Raport podaje tylko ścieżki.
- Zielony werdykt nie udaje kompletnego: sekcja „Pokrycie” podaje obie liczby.
