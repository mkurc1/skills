# Etykiety

Ten plik opisuje etykiety poza stanami: grupę, wyłączność, autora i skutek każdej. Czyta go skill `ba-github-issues`. Etykiety stanów stoją w [`statuses.md`](statuses.md).

## Grupy

| Grupa | Etykiety | Wyłączność | Kto nadaje |
|---|---|---|---|
| Priorytet | `priority-high`, `priority-medium`, `priority-low` | dokładnie jedna na issue | autor issue |
| Typ | `feat`, `bug` | najwyżej jedna, brak = GENERAL | autor issue |
| Sygnały PR-a | `blocked`, `hold` | dowolne | człowiek albo workflow review |

GENERAL to issue bez typu: nie jest ani funkcją, ani błędem.

## Skutek każdej etykiety

Opis i kolor to wartości etykiety w repozytorium. Z nich powstaje polecenie `gh label create`.

| Etykieta | Opis | Kolor | Skutek |
|---|---|---|---|
| `priority-high` | Release-blocking | `d93f0b` | Zadanie blokuje wydanie. |
| `priority-medium` | Ordinary bug or feature | `fbca04` | Zwykły błąd albo zwykła funkcja. |
| `priority-low` | Cosmetic or follow-up work | `e4e669` | Prace kosmetyczne albo kontynuacja. |
| `feat` | New capability | `a2eeef` | Nowa możliwość systemu. |
| `bug` | Something isn't working | `d73a4a` | Coś nie działa. |
| `blocked` | Blocked: waits for a human decision | `b60205` | PR czeka na decyzję człowieka. Agent nie rusza PR-a do zdjęcia etykiety. |
| `hold` | Pauses merging of the PR | `d4c5f9` | Wstrzymuje merge PR-a, automatyczny albo ręczny. Zdjęcie etykiety go odblokowuje. |

## Nazwy logiczne

Skille wskazują te etykiety nazwą logiczną. Prawdziwą nazwę bierzesz z tej tabeli.

| Nazwa logiczna | Etykieta |
|---|---|
| etykieta zablokowanego PR-a | `blocked` |
| etykieta wstrzymanego merge'a | `hold` |

## Reguły

- Każde issue ma dokładnie jedną etykietę priorytetu.
- Każde issue ma jedną etykietę z `feat` i `bug`, albo świadomie żadnej (GENERAL).
