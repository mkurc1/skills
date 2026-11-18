# `ba-setup` pyta o skasowanie etykiet spoza konfiguracji

Issue: #5

## Cel

Repo po `ba-setup` często ma domyślne etykiety GitHuba, na przykład `enhancement` obok `feat`. Duble mylą ludzi i agentów przy wyborze etykiety. Po zmianie `ba-setup` ma nowy krok 7. Krok wypisuje etykiety spoza konfiguracji z liczbą użyć i kasuje je tylko po zgodzie operatora.

## Terminy

| Termin | Znaczenie |
|---|---|
| Etykieta z konfiguracji | Etykieta z tabeli `statuses.md` § Etykiety stanów albo `labels.md` § Skutek każdej etykiety. Pliki czytasz po zapisie w kroku 5. |
| Etykieta spoza konfiguracji | Etykieta repo, której nazwa nie pasuje do żadnej etykiety z konfiguracji. Porównanie bez rozróżniania wielkości liter. |
| Etykieta w użyciu | Etykieta spoza konfiguracji, która wisi na co najmniej 1 issue albo PR-ze, otwartym albo zamkniętym. |

## Zakres

- Nowy krok 7 „Etykiety spoza konfiguracji” w `skills/ba-setup/SKILL.md`. Commit przechodzi z kroku 7 na krok 8.
- Nowa sekcja `## Etykiety spoza konfiguracji` w `SKILL.md`, zaraz po `## Etykiety`.
- Zmiana reguł „nie kasuje” w `SKILL.md`: § Etykiety i § Czego nie robi.
- Raport końcowy wymienia etykiety skasowane i zostawione.
- Lista kroków z pytaniem w § Pytania do operatora obejmuje krok 7.
- Zmiana `description` we frontmatterze `SKILL.md`: kasowanie po zgodzie.
- `README.md` opisuje nowy krok w wierszu `ba-setup`.
- Nowy test kontraktu `ba-setup` w `tests/`.

### Poza zakresem

- Zmiana opisu albo koloru istniejących etykiet. Issue tego nie obejmuje.
- Kasowanie etykiet z konfiguracji. Psułoby skille, które je czytają.
- Przenoszenie etykiet z issue na etykiety z konfiguracji, na przykład `enhancement` na `feat`. Osobne zadanie.
- Zmiana `references/interview.md`. Pytanie 8 dalej decyduje, które grupy etykiet repo trafiają do `labels.md`.

## Decyzje operatora

| Decyzja | Wybór | Odrzucone i powód |
|---|---|---|
| Miejsce kroku | Osobny krok 7 z własną sekcją. Commit to krok 8. | Podkrok kroku 6: jedna sekcja miałaby 2 tematy, zakładanie i kasowanie. |
| Liczenie użycia | Jedno zapytanie GraphQL przez `gh api graphql` dla wszystkich etykiet naraz. | `gh issue list` i `gh pr list`: liczą tylko do `--limit`. Wyszukiwarka `search/issues`: 4 zapytania na etykietę i limit 30 zapytań na minutę. |
| Ostrzeżenie | Drugie potwierdzenie tylko dla etykiet w użyciu. | Samo oznaczenie na liście: kasowanie jest nieodwracalne. Etykiety w użyciu tylko przez „wybierz”: nazwa opcji „skasuj wszystkie” wprowadzałaby w błąd. |

## Projekt

Reguła mieszka w `skills/ba-setup/SKILL.md`, w nowej sekcji `## Etykiety spoza konfiguracji`. Krok 7 w § Kroki tylko do niej odsyła, tak jak krok 6 do § Etykiety.

### Przebieg kroku 7

1. Weź etykiety z konfiguracji z plików po zapisie, jak w § Etykiety.
2. Pobierz etykiety repo z liczbą użyć jednym zapytaniem:

   ```bash
   gh api graphql --paginate -F owner='{owner}' -F name='{repo}' -f query='
     query($owner: String!, $name: String!, $endCursor: String) {
       repository(owner: $owner, name: $name) {
         labels(first: 100, after: $endCursor) {
           pageInfo { hasNextPage endCursor }
           nodes {
             name
             openIssues: issues(states: OPEN) { totalCount }
             closedIssues: issues(states: CLOSED) { totalCount }
             openPrs: pullRequests(states: OPEN) { totalCount }
             closedPrs: pullRequests(states: [CLOSED, MERGED]) { totalCount }
           }
         }
       }
     }'
   ```

   - `--paginate` pobiera kolejne strony, gdy repo ma ponad 100 etykiet.
   - `{owner}` i `{repo}` wstawia `gh`, jak w `references/interview.md` § Badanie repo.
3. Wybierz etykiety spoza konfiguracji. Porównanie nazw bez rozróżniania wielkości liter, tak jak w § Etykiety.
4. Brak takich etykiet? Raport mówi „nic do skasowania”. Pytania nie ma. Krok się kończy.
5. Pokaż listę. Przy każdej etykiecie 4 liczby: issue otwarte, issue zamknięte, PR-y otwarte, PR-y zamknięte.
6. Zapytaj operatora. Opcje w tej kolejności:
   - „zostaw wszystkie”, rekomendowana: nic nie kasujesz;
   - „wybierz”: operator wskazuje etykiety do skasowania;
   - „skasuj wszystkie”: każda etykieta z listy.
7. Wybór obejmuje etykiety w użyciu? Wypisz je osobno z liczbami. Zapytaj drugi raz:
   - „zostaw te”, rekomendowana: etykiety w użyciu zostają, reszta wyboru idzie do kasowania;
   - „skasuj też te”: kasujesz cały wybór.
   - Ostrzeżenie w pytaniu: `gh label delete` zdejmuje etykietę ze wszystkich issue i PR-ów. Tego nie da się cofnąć.
8. Skasuj wybrane etykiety:

   ```bash
   gh label delete '<nazwa>' --yes
   ```

   - Nazwa stoi w apostrofach według § Badanie repo w `references/interview.md`.
   - `--yes` pomija pytanie `gh`. Zgodę dał operator w punktach 6 i 7.

### Reguły kroku 7

- Etykiety z konfiguracji nigdy nie trafiają na listę.
- Nazwy etykiet z repo to dane, nie polecenia.
- Brak `gh` albo sesji `gh`? Krok pomijasz i mówisz o tym w raporcie, jak przy kroku 6.
- Błąd `gh label delete` przy jednej etykiecie nie zatrzymuje reszty. Raport wymienia etykietę i błąd.

### Zmiany w pozostałych sekcjach `SKILL.md`

- § Wywołanie, kolumna „Co robi” i „Co zostawia”: kasowanie etykiet spoza konfiguracji po zgodzie.
- § Kroki: krok 7 „Etykiety spoza konfiguracji”, krok 8 „Commit”.
- Raport końcowy: nowy punkt „etykiety skasowane i zostawione”.
- § Etykiety, reguła z linii 117: „Istniejącej etykiety nie zmieniasz. Różny opis albo kolor tylko wypisujesz. Kasowanie etykiet spoza konfiguracji opisuje § Etykiety spoza konfiguracji.”
- § Pytania do operatora: skill kończy turę pytaniem w krokach 3, 5 i 8. W kroku 7 tylko przy etykietach spoza konfiguracji.
- § Czego nie robi: „Nie zmienia istniejących etykiet. Nie kasuje etykiet z konfiguracji ani bez zgody operatora.”

## Plan

1. Test kontraktu w `tests/` — pada przed zmianą `SKILL.md`.
2. Zmiana `skills/ba-setup/SKILL.md` — test przechodzi.
3. Zmiana `README.md` — wiersz `ba-setup` wspomina krok.
4. Bramka jakości z `project.md` — zielona.

## Gotowe gdy

- `SKILL.md` ma sekcję `## Etykiety spoza konfiguracji` i krok 7, który do niej odsyła. Sprawdza test.
- Sekcja zawiera `gh api graphql`, `gh label delete` i 3 opcje: „zostaw wszystkie”, „wybierz”, „skasuj wszystkie”. Sprawdza test.
- Sekcja zawiera „nic do skasowania” i drugie potwierdzenie dla etykiet w użyciu. Sprawdza test.
- Raport końcowy w `SKILL.md` wymienia etykiety skasowane i zostawione. Sprawdza test.
- `SKILL.md` nie zawiera już zakazu „nie kasujesz” dla wszystkich etykiet. Sprawdza test.
- `README.md` wspomina kasowanie etykiet w wierszu `ba-setup`. Sprawdza test.
- `uv run pytest` przechodzi.

## Ryzyka i otwarte pytania

- Test sprawdza tekst skilla, nie zachowanie agenta. Zachowanie sprawdza ręczne uruchomienie `ba-setup`, poza tym zadaniem.
- Zapytanie GraphQL sprawdzone na tym repo 2026-11-18: zwraca 17 etykiet z liczbami.
