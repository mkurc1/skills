# Proces dostarczania zmian

Ten plik pokazuje drogę zadania od issue do PR-a zmergowanego do `main`. Mówi, kto prowadzi każdy etap i kiedy etap się kończy.

- Zadania i PR-y żyją w GitHubie. Repozytorium podaje [`project.md`](../config/project.md#repozytorium).
- Repo nie ma pliku z regułami pracy agenta. Reguły procesu stoją w tym pliku i w `.ai/config/`.
- Wartości projektu stoją w `.ai/config/`. Ten plik do nich linkuje.
- Nowe repo dostaje `.ai/config/` i ten plik ze skilla `ba-setup`.

## Cykl życia zadania

Zadanie przechodzi te etapy w tej kolejności. Etap Specyfikacja dotyczy każdego issue, także błędu.

| Etap | Co się dzieje | Kto prowadzi | Koniec, gdy |
|---|---|---|---|
| Zgłoszenie | Issue opisuje problem i stan „gotowe”. Treść idzie według [szablonu issue](../config/issue-template.md). | Człowiek, `ba-refine-issue` albo `ba-github-issues create` | Issue spełnia [Definition of Ready](../config/definition-of-ready.md) |
| Przejęcie | Autor bierze zadanie i zakłada gałąź. Zasady w § Przejęcie pracy. | `ba-github-issues start` albo łańcuch `ba-fix-issue` lub `ba-auto-fix-issue` | Issue ma assignee i etykietę stanu `in-progress` z [`statuses.md`](../config/statuses.md#stany) |
| Specyfikacja | Każde issue dostaje specyfikację i plan w `.ai/specs/` przed kodem. | Człowiek, `ba-plan` (z operatorem albo `--auto`) albo łańcuch `ba-fix-issue` lub `ba-auto-fix-issue` | Specyfikacja zatwierdzona |
| Implementacja | Autor pisze zmianę z testami. Bramka jakości przechodzi lokalnie. | Człowiek, `ba-implement` albo łańcuch `ba-fix-issue` lub `ba-auto-fix-issue` | [Bramka jakości](../config/project.md#bramka-jakości) zielona |
| PR | Gałąź dostaje lokalne review, commit, push i PR do `main`. Fakty o PR-ach: [`pull-request.md`](../config/pull-request.md). | `ba-ship-pr`, który czeka przez `ba-wait-checks` | Otwarty PR z wypełnionym opisem i wynikiem każdego sprawdzenia |
| Review | Człowiek ocenia diff w PR-ze. Reguły review: [`code-review.md`](../config/code-review.md). | Recenzent | Recenzent zostawił uwagi albo zatwierdzenie |
| Merge | Człowiek merguje PR po zielonych checkach. | Opiekun repo | PR zmergowany, issue zamknięte |

Zmiana w interfejsie wymaga sprawdzenia w przeglądarce. Wymóg stoi w [DoD](../config/definition-of-done.md#41-feature).

Proces kończy się na merge.

## Który łańcuch

Dwa łańcuchy prowadzą issue od przejęcia do PR-a. Różnią się tym, kto pisze specyfikację.

- `/ba-fix-issue <n>`: specyfikację piszesz razem z operatorem, on ją akceptuje, potem praca idzie sama. Wybierz go dla nowej funkcjonalności, decyzji z [listy opiekuna](../config/project.md#decyzje-opiekuna) i niejasnego zakresu.
- `/ba-auto-fix-issue <n>`: agent pyta raz i pisze specyfikację sam. Wybierz go dla błędu i zadania z jasnym zakresem.

Oba łańcuchy działają tylko na jawne wywołanie operatora.

## Role

- **Autor** pisze zmianę. Odpowiada za zadanie od przejęcia do PR-a gotowego do merge.
- Autorem bywa człowiek albo agent.
- **Recenzent** to człowiek. Ocenia diff według [`code-review.md`](../config/code-review.md).
- **Opiekun repo** odpowiada za ochronę gałęzi `main`, etykiety, `.ai/config/` i ten plik.

## Stany i etykiety

Stan zadania to stan issue plus etykieta stanu. Stany i przejścia definiuje [`statuses.md`](../config/statuses.md).

Pozostałe etykiety i ich skutek opisuje [`labels.md`](../config/labels.md).

## Przejęcie pracy

**Assignee plus etykieta stanu `in-progress`** znaczy: zadanie zajęte. Nazwę etykiety podaje [`statuses.md`](../config/statuses.md#stany).

- Autor nadaje oba sygnały przed pierwszą zmianą.
- Inny autor nie rusza zajętego zadania.
- Autor przerywa pracę bez zamknięcia issue? Zwalnia zadanie przez `ba-github-issues release <n> <powód>`.
- Ta sama zasada obowiązuje po porażce.
- Skutki operacji opisuje skill. Stany, w tym stan po zwolnieniu (`todo`), opisuje [`statuses.md`](../config/statuses.md#stany).

Oba sygnały nadaje `ba-github-issues start`. Domknięcie issue robi `ba-github-issues close`.

## Bramki

Zadanie przechodzi 3 bramki.

1. **Wejście:** [Definition of Ready](../config/definition-of-ready.md).
2. **Wyjście:** [Definition of Done](../config/definition-of-done.md).
3. **Przed merge:** wymagane checki CI. Lista: [`pull-request.md` § Checki w CI](../config/pull-request.md#checki-w-ci).

Szczegóły checków przed merge:

- Opis PR-a: [`pull-request.md` § Opis PR-a](../config/pull-request.md#opis-pr-a).
- Merge i etykieta wstrzymanego merge'a: [`pull-request.md` § Merge](../config/pull-request.md#merge).

## Łączenie skilli

Skill woła inny skill tylko przez jego sekcję `## Wywołanie`. Nigdy nie wskazuje sekcji ani kroku innego skilla.

- Dobrze: „skill `ba-github-issues start <n>`”.
- Źle: numer sekcji albo kroku z treści innego skilla.
- Zmiana wnętrza skilla nie psuje wołających, dopóki kontrakt `## Wywołanie` zostaje.
- Regułę pilnuje test `tests/test_skill_contracts.py`.

## Zmiana procesu

Każda zmiana procesu trafia w jedno miejsce.

| Zmiana | Gdzie |
|---|---|
| Nowy stan zadania | [`statuses.md`](../config/statuses.md) i tabela cyklu w tym pliku |
| Nowa etykieta | [`labels.md`](../config/labels.md), z opisem i kolorem |
| Nowy etap albo nowa rola | Ten plik |
