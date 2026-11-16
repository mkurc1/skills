---
name: ba-auto-fix-issue
description: Use ONLY when the user explicitly runs /ba-auto-fix-issue <issue number> or directly asks to carry out a GitHub issue end to end on its own ("zrób issue 123 automatem", "zrealizuj issue sam"). It runs the building-block skills: ba-github-issues start (claims the issue first) → ba-plan → ba-implement → ba-ship-pr. ba-plan reads the docs, checks the issue has everything it needs and asks the user once about missing data and open decisions; after that the chain works alone up to the PR, stopping only on the listed blockers. Running it is the user's explicit consent for commit, push and PR creation through ba-ship-pr. Never auto-invoke it from repo state or from a plain "zacznij issue 123".
---

# /ba-auto-fix-issue — issue od numeru do PR-a

Wejście: numer issue. Wynik: wystawiony PR, który `ba-ship-pr` prowadzi do zielonych checków.

Ten skill to łańcuch. Łańcuch woła klocki w ustalonej kolejności. Klocek to skill z jednym zadaniem i kontraktem `## Wywołanie`.

- `ba-github-issues start` zajmuje issue na starcie. Niegotowe issue zatrzymuje łańcuch.
- `ba-plan` pisze specyfikację i plan. Pyta raz o braki i decyzje.
- `ba-implement` wykonuje plan i commituje.
- `ba-ship-pr` wystawia PR i prowadzi go do zielonych checków.

Reguły pracy mieszkają w klockach i w `.ai/config/`. Nie powielaj ich tutaj.

## Wywołanie

| Wywołanie | Co robi | Co zostawia |
|---|---|---|
| `/ba-auto-fix-issue <n>` | Prowadzi issue `<n>` od odczytu do PR-a | Wystawiony PR i raport końcowy |

## Kroki

Załóż zadanie (TaskCreate) na każdy krok i idź po kolei. Klocki wołasz tylko przez ich `## Wywołanie`.

1. **Klocki.** Sprawdź, czy są dostępne `ba-github-issues`, `ba-plan`, `ba-implement`, `ba-ship-pr` i `ba-wait-checks`.
   - Źródło: lista skilli narzędzia albo plik `SKILL.md` w katalogu skilli projektu.
   - Brak klocka zatrzymuje pracę. Podaj operatorowi nazwę brakującego skilla.
2. **Odczyt.** Skill `ba-github-issues read <n>`. Sprawdź stan startowy z sekcji „Kiedy stajesz”.
3. **Start.** Skill `ba-github-issues start <n>`.
   - Zajmuje issue od razu: etykieta stanu, assignee, gałąź.
   - Issue jest gotowe przed uruchomieniem łańcucha. Niegotowe zatrzymuje się na sprawdzeniu gotowości w `start`.
4. **Specyfikacja i plan.** Skill `ba-plan <n> --auto`.
   - Pytania `ba-plan` kończą turę. Po odpowiedzi operatora wracasz do tego kroku.
5. **Implementacja.** Skill `ba-implement <n>`.
6. **Wysyłka.** Skill `ba-ship-pr`.
   - Wywołanie `/ba-auto-fix-issue` jest zgodą operatora na commit, push i PR.
   - Wybory z dziennika `ba-implement` wpisz do opisu PR-a, w sekcji `## Co się zmienia`.
7. **Raport końcowy.** Dołącz go do komunikatu, którym `ba-ship-pr` kończy pierwszą turę. Kształt: sekcja „Raport końcowy”.

## Kiedy stajesz

Łańcuch kończy turę pytaniem do operatora tylko w tych przypadkach:

- **Stan startowy**: niezacommitowane zmiany w drzewie poza plikami w `.ai/specs/`. Issue zamknięte albo z otwartym PR-em.
- **Brak klocka** z kroku 1.
- **Niegotowe issue** w kroku 3: `start` zgłasza braki według DoR.
- **Awaria infrastruktury** w kroku łańcucha: brak sieci albo sesji `gh`.
- **Pytania `ba-plan`** o braki i decyzje.
- **Każde zatrzymanie `ba-implement`.**
- **Każde zatrzymanie `ba-ship-pr`.**

Każde zatrzymanie to pauza, nie porzucenie:

- Pytanie ma opcje do wyboru. Formę podaje `.ai/config/project.md` § Pytania do operatora.
- Raport mówi: co blokuje, co sprawdziłeś, stan gałęzi.
- Zadanie zostaje zajęte, dopóki operator nie zdecyduje.

Jedna z opcji brzmi „porzuć zadanie”. Po jej wyborze (i tylko wtedy) zwolnij zadanie: skill `ba-github-issues release <n> <powód>`.

- Dotyczy to zatrzymania po kroku 3, także w trakcie rozmowy o specyfikacji.
- Przed krokiem 3 nic nie zwalniasz. Nikt jeszcze nie przejął zadania.

## Raport końcowy

```
**PR:** <url>
- Sprawdzenia: stan każdego z raportu ba-wait-checks, czerwone z werdyktem winy
- Co się zmieniło: 1-3 punkty
- Odpowiedzi operatora z ba-plan: lista albo „Brak pytań"
- Wybory z ba-implement (z dziennika): lista z powodem
- Druga droga weryfikacji: co i z jakim wynikiem
- Skille niedostępne, krok zrobiony ręcznie: z dziennika albo „Brak"
- Założone issue: #n tytuł
- Po wdrożeniu: kroki albo „Brak"
```
