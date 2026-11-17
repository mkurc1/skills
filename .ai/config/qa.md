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

Repo nie ma aplikacji do testu w przeglądarce. Skill `ba-qa` nie ma tu zastosowania.

## Adres

Brak. Repo nie ma aplikacji do testu w przeglądarce. Skill `ba-qa` nie ma tu zastosowania.

## Logowanie

Aplikacja nie ma logowania.

## Konta testowe

Aplikacja nie ma kont.

## Sprzątanie

Nic do sprzątania. Repo nie ma aplikacji ani bazy.

## Zrzuty ekranu

Brak. Repo nie ma aplikacji, więc nie ma zrzutów.

## Testy E2E

Repo nie ma stałych testów E2E.
