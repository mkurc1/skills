# Dziennik: `ba-setup` pyta o skasowanie etykiet spoza konfiguracji

Issue: #5

Plan: [`.ai/specs/implemented/2026-11-18-setup-delete-extra-labels-plan.md`](../specs/implemented/2026-11-18-setup-delete-extra-labels-plan.md)

## Postęp

- [x] Task 1: test kontraktu, `6a1bf45`. Przed zmianą 6 testów FAIL.
- [x] Task 2: krok 7 w `SKILL.md`, `1a39568`. 5 z 6 testów PASS, `README.md` jeszcze FAIL.
- [x] Task 3: `README.md` i bramka. Bramka zielona: 87 testów PASS, `ruff` czysty.

## Wybory

- Plan wykonany w głównej sesji, zadanie po zadaniu, bez podagenta na zadanie. Powód: 3 małe zmiany tekstu i jeden plik testu. Recenzję całej gałęzi robi świeży podagent i lokalne review `ba-ship-pr`.
- Commity mają autora operatora przez zmienne `GIT_AUTHOR_*`. Powód: worktree nie ma `user.name` w konfiguracji gita. Konfiguracji nie zmieniałem.
- Recenzja całej gałęzi zostaje dla lokalnego review w `ba-ship-pr`.

## Weryfikacja

- Bramka jakości: `uv sync --locked`, `ruff check`, `ruff format --check`, `pytest`. 87 PASS.
- Mutacja: `SKILL.md` i `README.md` cofnięte do `main`. `tests/test_setup_extra_labels.py` daje 6 FAIL. Po przywróceniu 6 PASS.
- Druga droga: zapytanie GraphQL wycięte z `SKILL.md` i uruchomione na `mkurc1/skills`. Zwraca 17 etykiet z liczbami. Spoza konfiguracji wychodzi 9: `accessibility`, `documentation`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix`. Zgodne z § Dowód w issue.

## Lokalne review (`ba-ship-pr`, runda 1)

- 3 audytorów, potem `code-review:challenger`. `code-review:cross-verifier` pominięty: znaleziska z 2 audytorów pokrywały się, challenger je sprawdził.
- Zastosowane:
  - Krok 7 pomija się bez tabel etykiet w konfiguracji. Powód: etykiety skilli trafiłyby na listę.
  - Reguły o braku `gh` i nazwach jako danych zastąpione odsyłaczem do `references/interview.md`. Powód: jedna reguła w jednym miejscu.
  - Test listy kroków kończących turę. Powód: cofnięcie tej linii nie łamało testów.
  - `gh label delete --yes -- '<nazwa>'`. Powód: nazwa z `-` na początku byłaby flagą. Sprawdzone: `gh` bierze nazwę po `--`.
  - Ostrzeżenie wspomina dyskusje. Powód: licznik ich nie obejmuje.
- Odrzucone: ograniczenie „wybierz” do listy. Challenger: fałszywy alarm, liczby są dla wszystkich etykiet, a § Czego nie robi zakazuje kasowania etykiet z konfiguracji.
- Mutacja 3 nowych asercji: każda pada po cofnięciu swojej zmiany.

## Lokalne review, runda 2

- Audytor jakości z zakresem bezpieczeństwa i dokumentacji. 2 MEDIUM, 2 LOW.
- Zastosowane:
  - Trafienie nazwy w `.github/` też oznacza etykietę w użyciu. Powód: workflow albo Dependabot traci etykietę bez ostrzeżenia. Źródło: pytanie 8 w `references/interview.md` uznaje to za dowód użycia.
  - Test zabezpieczeń sekcji: brak etykiet z konfiguracji na liście, ostrzeżenie, dyskusje, błąd jednej etykiety, `.github/`.
  - Plan ma nowe polecenie `gh label delete --yes -- '<nazwa>'`.
  - Dziennik ma aktualne liczby testów niżej.

## Lokalne review, runda 3

- 2 MEDIUM, oba zastosowane:
  - Dowód użycia odsyła do pytania 8 w `references/interview.md`. Powód: druga, węższa kopia warunku.
  - Ostrzeżenie o dyskusjach i nieodwracalności stoi przy pierwszym pytaniu. Powód: etykieta z samymi zerami nie dostaje drugiego pytania.
- Limit 3 rund wyczerpany. Poprawek z rundy 3 nie sprawdzała już 4. runda. Push czeka na decyzję operatora.
- Bramka po rundzie 3: 91 PASS. Mutacja: ostrzeżenie przeniesione z powrotem do punktu 7 daje FAIL nowego testu.

## Lokalne review, runda 4 (na prośbę operatora)

- 2 MEDIUM, oba zastosowane:
  - Test zabezpieczeń pilnuje zdania „Lista pokazuje plik trafienia”. Mutacja: usunięcie zdania daje FAIL.
  - Dziennik ma liczby po rundzie 3 i mutację testu pozycji ostrzeżenia.
- Bramka po rundzie 4: 91 PASS, `ruff` czysty.
- Commit autosave cezara wciągnął `.claude/scratch/`. Commit był tylko lokalny, cofnięty. `.claude/scratch/` dopisany do lokalnego `info/exclude`.

## Wysyłka

- Operator wybrał push i PR po rundzie 4.
- Specyfikacja i plan przeniesione do `.ai/specs/implemented/`.
- Follow-up: issue #7, ignorowanie `.claude/scratch/` w `ba-ship-pr`.
