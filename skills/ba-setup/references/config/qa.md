# Konfiguracja QA w przeglądarce

Ten plik podaje skillowi `ba-qa` fakty o projekcie: jak wstaje aplikacja, pod jakim adresem stoi, jak zalogować testera i gdzie leżą zrzuty ekranu.

Skill czyta sekcje po nazwie. Nie zmieniaj nagłówków `## ` i nie usuwaj sekcji.

| Sekcja | Cel |
|---|---|
| Start aplikacji | Podaje komendy, które uruchamiają aplikację, i sprawdzenie gotowości każdej usługi. |
| Adres | Podaje adres aplikacji, pod którym testuje przeglądarka. |
| Logowanie | Mówi, jak wstrzyknąć sesję zalogowanego użytkownika do przeglądarki. |
| Konta testowe | Podaje komendy, które zakładają konta testowe z rolami. |
| Sprzątanie | Mówi, co przejście usuwa po teście, a czego nie rusza. |
| Zrzuty ekranu | Podaje katalog zrzutów. Katalog jest poza historią repozytorium. |
| Testy E2E | Podaje katalog i komendę stałych testów całej aplikacji. |

Komendy działają z katalogu głównego repozytorium. Zmianę katalogu zamyka podpowłoka `( cd … && … )`.

## Start aplikacji

Uruchom usługi po kolei. Każda ma przejść sprawdzenie gotowości, zanim ruszy następna.

| Usługa | Komenda | Gotowość |
|---|---|---|
| {usługa, na przykład baza} | `{komenda uruchomienia}` | `{komenda, która sprawdza gotowość}` |
| {usługa, na przykład API} | `{komenda uruchomienia}` | `{komenda, która sprawdza gotowość}` |
| {usługa, na przykład frontend} | `( cd {katalog} && {komenda uruchomienia} )` | `{komenda, która sprawdza gotowość}` |

Usługa działa już? Nie uruchamiaj jej drugi raz. Usługa z kodem aplikacji ma działać z tego repozytorium. {Komenda, która pokazuje katalog główny repozytorium procesu na porcie.}

{Zakaz destrukcyjnej komendy bazy, gdy repo ją ma, na przykład reset całej bazy. Usuń zdanie, gdy brak.}

## Adres

`{adres aplikacji, na przykład http://localhost:3000}`

## Logowanie

{Jak zalogować testera w przeglądarce: skill logowania z `.agents/skills/`, wstrzyknięcie sesji do `localStorage`, formularz z kontem testowym. Podaj kroki i sygnał zalogowania, na przykład przycisk widoczny tylko po zalogowaniu. Aplikacja bez logowania: napisz „Aplikacja nie ma logowania.” i usuń resztę.}

Sesja jest żywym tokenem. Token i nagłówek `Authorization` nie trafiają do żadnego pliku ani commita.

## Konta testowe

| Rola | Komenda |
|---|---|
| `{rola, na przykład user}` | `{komenda, która zakłada konto testowe}` |
| `{rola, na przykład admin}` | `{komenda, która zakłada konto testowe}` |

{Czy komenda jest idempotentna i gdzie odmawia pracy, na przykład w produkcji. Aplikacja bez kont: napisz „Aplikacja nie ma kont.” i usuń tabelę.}

{Działania zakazane w przejściu: akcje w interfejsie, które kasują dane, należą do właściciela albo kosztują. Dopisz zakaz zmiany danych, których przejście nie założyło, z wyjątkiem konta testowego i wierszy z pliku identyfikatorów. Aplikacja bez takich akcji: zostaw sam zakaz.}

## Sprzątanie

{Co przejście usuwa po teście i jak: komenda albo przycisk w interfejsie. Co zostaje, na przykład konto współdzielone z CI.}

{Dane startowe wstawiane komendą: zwykły `INSERT` zwracający identyfikatory, bez nadpisywania przy konflikcie. Identyfikatory w pliku `{ścieżka w katalogu z .gitignore, na przykład .playwright-mcp/qa-seed-ids.txt}` od razu po wstawieniu. Usunięcie tylko po identyfikatorach z tego pliku. Po udanym usunięciu skasuj wpis z pliku. Zakaz destrukcyjnego SQL i zmian istniejących wierszy. Usuń zdanie, gdy repo nie ma bazy.}

## Zrzuty ekranu

`{katalog zrzutów, na przykład .playwright-mcp/}`

Katalog jest w `.gitignore`. Zrzuty nie trafiają do commita.

## Testy E2E

- Katalog testów: `{katalog, na przykład e2e/}`
- Uruchomienie: `{komenda uruchamiająca stałe testy E2E}`

{Repo bez stałych testów E2E: napisz „Repo nie ma stałych testów E2E.” i usuń listę.}
