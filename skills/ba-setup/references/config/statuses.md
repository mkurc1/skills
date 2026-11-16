# Stany zadania

Ten plik definiuje stany zadania i etykietę każdego stanu. Czyta go skill `ba-github-issues`, a proces opisuje `.ai/docs/sdlc.md`.

## Stany

| Stan | Stan issue | Etykieta | Assignee | Kto wprowadza |
|---|---|---|---|---|
| `todo` | open | — | — | założenie issue albo `ba-github-issues release` |
| `in-progress` | open | `in-progress` | wymagany | `ba-github-issues start` |
| `done` | closed `completed` | — | — | merge PR-a z `Closes #n` albo `ba-github-issues close` |
| `dropped` | closed `not planned` | — | — | `ba-github-issues close` |

## Reguły

- Issue ma najwyżej jedną etykietę stanu.
- Wejście w stan zdejmuje etykiety pozostałych stanów.
- Krok `ba-github-issues close` zdejmuje etykiety stanów przy zamknięciu issue.
- {Workflow repo, który zdejmuje etykietę stanu przy zamknięciu, wpisz tutaj. Usuń, gdy brak.}
- Nowy stan to nowy wiersz tabeli. `SKILL.md` się nie zmienia.

## Etykiety stanów

Każda etykieta stanu ma opis i kolor. Z nich powstaje polecenie `gh label create`.

| Etykieta | Opis | Kolor |
|---|---|---|
| `in-progress` | An automated skill is working on this | `c5def5` |

```bash
gh label create 'in-progress' --description 'An automated skill is working on this' --color 'c5def5'
```
