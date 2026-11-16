---
name: ba-implement
description: Use when an issue already has a spec and a plan in .ai/specs/ and the code must be built — executes the plan task by task (fresh subagent and review per task when available), stops on any operator decision missing from the spec, verifies twice and commits. Refuses to start without the spec and plan. Does not push or open a PR. Called by ba-auto-fix-issue and ba-fix-issue; also runnable alone as /ba-implement <n>.
---

# /ba-implement — wykonanie planu dla issue

Wejście: numer issue. Wynik: commity na gałęzi zadania, dziennik w `.ai/runs/` i zielona bramka jakości.

- Skill nie startuje bez specyfikacji i planu.
- Skill nie wypycha gałęzi.
- Skill nie wystawia PR-a.

Wiedzę o projekcie skill bierze z `.ai/config/`. Reguły projektu mieszkają tam i w plikach, do których te pliki odsyłają.

## Wywołanie

| Wywołanie | Co robi | Co zostawia |
|---|---|---|
| `/ba-implement <n>` | Wykonuje plan i specyfikację z linią `Issue: #<n>` zadanie po zadaniu. | Commity na gałęzi zadania, dziennik w `.ai/runs/`, zieloną bramkę jakości. Bez pusha i bez PR-a. |

## Konfiguracja

Na początku pracy przeczytaj te pliki z `.ai/config/`:

| Plik | Co daje |
|---|---|
| `project.md` | sekcje „Gałąź”, „Dobór skilli”, „Decyzje opiekuna”, „Bramka jakości”, „Pytania do operatora”, „Zgłaszanie błędów spoza zakresu” |
| `spec-template.md` | szablon specyfikacji: wersja pełna i wersja krótka dla błędu |
| `plan-template.md` | szablon planu |
| `definition-of-ready.md` | warunki gotowości issue |

**Brak pliku** zatrzymuje skill. Podaj operatorowi nazwę brakującego pliku. Brakujące pliki generuje skill `ba-setup`.

## Kroki

Załóż zadanie (TaskCreate) na każdy krok i idź po kolei. Krok 1 to sekcja „Konfiguracja”.

2. **Specyfikacja i plan.** Szukaj w `.ai/specs/*.md` specyfikacji i planu z linią issue.
   - Linia issue to `Issue: #<n>` albo `**Issue:** #<n>`. Po numerze nie stoi cyfra. Dla `#101` linia `Issue: #1018` nie pasuje.
   - Plan to plik z końcówką `-plan.md` i linią `Specyfikacja:` z linkiem do jego specyfikacji. Specyfikacja to drugi plik pary.
   - Pomijasz katalogi `implemented/` i `archive/`.
   - Brak specyfikacji albo planu zatrzymuje pracę. Komunikat: „Brak specyfikacji albo planu dla #<n>. Najpierw `/ba-plan <n>`.”
   - Więcej niż jedna para dla `#<n>` daje pytanie do operatora, którą wziąć.
   - Przeczytaj obie części w całości przed pierwszą zmianą.
3. **Gałąź.** Nazwa bieżącej gałęzi pasuje do wzorca z sekcji „Gałąź” w `project.md` dla numeru `<n>`.
   - Przykład wzorca: `<typ>/<n>-<slug>`. Sam numer w nazwie nie wystarcza.
   - Inna gałąź zatrzymuje pracę. Komunikat: „Najpierw `ba-github-issues start <n>`.”
4. **Dziennik.** Załóż `.ai/runs/YYYY-MM-DD-slug.md` przed pierwszą zmianą kodu.
   - Datę bierzesz z `date +%F`. Slug jest taki sam jak w specyfikacji.
   - Dziennik ma link do planu.
   - Prowadź w nim postęp zadań i wybory z kroku 6.
5. **Wykonanie planu.** Użyj skilla z wiersza „Wykonanie planu” w sekcji „Dobór skilli” w `project.md`.
   - **Ustawienia z góry** podajesz skillowi wykonawczemu. Skill wykonawczy nie pyta o nie operatora:
     - praca w bieżącym katalogu, na bieżącej gałęzi;
     - bez nowego worktree i bez izolowanego katalogu roboczego;
     - sposób wykonania: podagent na zadanie z recenzją po każdym zadaniu.
   - **Zasady stopu** z tego skilla są wiążące dla skilla wykonawczego. Strażnik nr 2 i sekcja „Kiedy stajesz” mają pierwszeństwo przed jego własnymi zasadami. Jego reguła „decyduj, nie stawaj” ich nie uchyla. Podajesz mu je jako twarde ograniczenia.
   - **Rozstrzygnięcia skilla wykonawczego** przepisujesz do dziennika w `.ai/runs/`. Jego prywatne notatki mogą leżeć w pliku ignorowanym przez git.
   - **Koniec pracy** następuje po recenzji całej gałęzi. Krok „zakończ gałąź” skilla wykonawczego się nie odbywa. PR robi osobny skill wysyłki.
   - **Bez skilla wykonawczego** dajesz każdemu zadaniu własnego podagenta i recenzję po zadaniu. Bez podagentów idziesz zadanie po zadaniu i sprawdzasz każde sam.
   - **Test przed kodem.** Skille i agentów w zadaniach dobierasz według sekcji „Dobór skilli”.
   - **Agenci edytujący pliki** pracują po kolei. Nigdy nie pracują równolegle na jednym katalogu roboczym.
6. **Strażnik nr 2.** Wybór, który jest decyzją opiekuna, a którego nie ma w specyfikacji, zatrzymuje pracę. Szczegóły: sekcja „Strażnik decyzji opiekuna”.
7. **Weryfikacja.** Wynik sprawdzasz dwa razy, dwiema niezależnymi drogami.
   - Uruchom bramkę jakości z sekcji „Bramka jakości” w `project.md`. Bramka ma być zielona.
   - Druga droga jest niezależna od testów z kroku 5. Przykład: uruchomienie na danych spreparowanych pod przypadek.
   - Nowy albo zmieniony test regresyjny przechodzi weryfikację mutacyjną. Weryfikacja mutacyjna to sprawdzenie, że test pada po cofnięciu poprawki. Skill do niej podaje sekcja „Dobór skilli”.
   - Raport podagenta sprawdzasz sam. Deklaracja „testy przechodzą” nie jest dowodem.
8. **Dokumentacja.** Użyj skilla z wiersza o dokumentacji w sekcji „Dobór skilli”.
9. **Commit.** Zacommituj specyfikację, plan, kod, testy i dziennik na gałęzi zadania.
   - Commit nie ma podpisu agenta.
   - Nie wypychasz gałęzi i nie wystawiasz PR-a.

Skill albo agent z sekcji „Dobór skilli” jest niedostępny w środowisku? Zrób ten krok sam i zapisz to w dzienniku. To nie jest powód do stopu. Dotyczy kroków 5, 7 i 8.

## Strażnik decyzji opiekuna

Decyzja opiekuna to decyzja z listy w sekcji „Decyzje opiekuna” w `project.md`. Agent nie podejmuje jej sam.

Wybór odkryty w trakcie implementacji sprawdzasz z tą listą:

- **Wybór z listy, którego nie ma w specyfikacji**, zatrzymuje pracę. Zadajesz pytanie z opcjami i rekomendacją. Formę podaje sekcja „Pytania do operatora”.
- **Zatwierdzony wybór** dopisujesz do specyfikacji. Potem wracasz do kroku 5.
- **Wybór spoza listy** rozstrzygasz sam według sekcji „Wybór w trakcie implementacji”. Zapisujesz go w dzienniku.

## Prostota

Rozwiązujesz to issue, nic więcej. Wybierasz najmniejszą zmianę, która spełnia specyfikację.

Porządki poza zakresem issue zostaw. Wyjątkiem jest drobiazg w dotykanym pliku: literówka albo nieaktualny komentarz.

## Znaleziska poza zakresem

Realny problem z dowodem w kodzie albo w danych dostaje issue. Problem hipotetyczny nie dostaje issue.

- Issue zakładasz skillem `ba-github-issues create`.
- Czy pytać operatora przed założeniem, podaje sekcja „Zgłaszanie błędów spoza zakresu” w `project.md`.
- Numer issue trafia do dziennika.

Znaleziska nie naprawiasz po cichu.

## Wybór w trakcie implementacji

Wybór spoza listy decyzji opiekuna rozstrzygasz sam:

1. Sprawdź dokumentację projektu i najbliższy istniejący kod. Zwykle odpowiedź już tam jest.
2. Wybierz opcję prostszą i zgodną z tymi źródłami.
3. Zapisz wybór i powód w dzienniku.

Zmiana łamie granice modułów, które sprawdza narzędzie z bramki jakości? Przeprojektuj ją tak, żeby zależność szła w dozwoloną stronę. Wyjątku w konfiguracji tego narzędzia nie dopisujesz.

## Kiedy stajesz

Poza krokami 2, 3 i strażnikiem tylko tutaj kończysz turę pytaniem do operatora:

- **Awaria infrastruktury**: brak sieci, bazy, zmiennych środowiskowych, sesji narzędzia do issue albo kontenerów.
- **Bramka jakości** czerwona po 3 próbach naprawy przyczyny.
- **Issue** okazuje się w trakcie implementacji sprzeczne, niewykonalne, za duże na jeden PR albo łamie regułę krytyczną projektu.
- **Operacja destrukcyjna** na bazie. Obejmuje każdą migrację kasującą dane.
- **Zapis do bazy produkcyjnej**. Migracja trafia na produkcję tylko przez wdrożenie po scaleniu.
- **Granica modułów**: żaden projekt zmiany nie mieści się w regułach narzędzia z bramki jakości.

Bramki przechodzą na zielono zawsze. Nie wyłączasz testu, nie obniżasz progu, nie dodajesz wyjątków lintera ani typów, żeby je uciszyć.

Każde zatrzymanie to pauza:

- Pytanie ma opcje do wyboru. Formę podaje sekcja „Pytania do operatora”.
- Raport mówi: co blokuje, co sprawdziłeś, stan gałęzi.
- Po pytaniu kończysz turę.
- Zwolnienie zadania to decyzja łańcucha, który wołał skill, albo operatora. Ten skill zadania nie zwalnia.
