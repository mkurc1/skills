---
name: ba-plan
description: Use when an issue needs a spec and an implementation plan before any code. By default writes the spec together with the operator (questions one at a time, 2–3 approaches, explicit acceptance), then writes the plan alone; with --auto asks once and writes both alone. Reads the issue, project docs and templates in .ai/config/; never writes code or creates a branch. Called by ba-fix-issue (default) and ba-auto-fix-issue (--auto); also runnable alone as /ba-plan <n> [--auto].
---

# /ba-plan — specyfikacja i plan dla issue

Wejście: numer issue. Wynik: specyfikacja i plan w `.ai/specs/`, gotowe do implementacji, oraz komentarz z planem w issue.

Skill ma 2 tryby:

- **Domyślny.** Specyfikację piszesz razem z operatorem w rozmowie. Operator ją akceptuje. Plan piszesz sam.
- **`--auto`.** Pytasz raz o braki i decyzje. Specyfikację i plan piszesz sam.

- Skill nie pisze kodu.
- Skill nie zakłada gałęzi.
- Skill nie commituje specyfikacji ani planu.
  Commit robi `ba-implement`. Gdy gałęzi zadania jeszcze nie ma, nieśledzone pliki przechodzą na nią przy jej założeniu.

Wiedzę o projekcie skill bierze z `.ai/config/`. Reguły projektu mieszkają tam i w plikach, do których te pliki odsyłają.

## Wywołanie

| Wywołanie | Co robi | Co zostawia |
|---|---|---|
| `/ba-plan <n>` | Specyfikację piszecie razem, operator ją akceptuje, plan agent pisze sam. | `.ai/specs/YYYY-MM-DD-slug.md` z linią `Issue: #<n>` i `.ai/specs/YYYY-MM-DD-slug-plan.md`, bez commita. Komentarz z planem w issue. |
| `/ba-plan <n> --auto` | Pyta raz o braki i decyzje, specyfikację i plan pisze sam. | To samo. |

## Konfiguracja

Na początku pracy przeczytaj te pliki z `.ai/config/`:

| Plik | Co daje |
|---|---|
| `project.md` | sekcje „Dokumentacja przed pracą”, „Dobór skilli”, „Decyzje opiekuna”, „Pytania do operatora” |
| `spec-template.md` | szablon specyfikacji: wersja pełna i wersja krótka dla błędu |
| `plan-template.md` | szablon planu |
| `definition-of-ready.md` | warunki gotowości issue |

**Brak pliku** zatrzymuje skill. Podaj operatorowi nazwę brakującego pliku. Brakujące pliki generuje skill `ba-setup`.

## Kroki

Załóż zadanie (TaskCreate) na każdy krok i idź po kolei. Krok 1 to sekcja „Konfiguracja”. Kroki 1-5 są wspólne dla obu trybów.

2. **Odczyt.** Sprawdź `git status`.
   - Drzewo robocze ma być czyste. Wyjątkiem są pliki w `.ai/specs/`.
   - Przeczytaj issue z komentarzami: skill `ba-github-issues read <n>`.
   - Szukaj w `.ai/specs/` specyfikacji albo planu z linią issue. Zasada: sekcja „Istniejąca specyfikacja”.
3. **Dokumentacja.** Przeczytaj źródła z sekcji „Dokumentacja przed pracą” w `project.md`.
   - Rób to, zanim dotkniesz kodu i zanim zadasz pytanie.
   - Potem prześledź ścieżkę kodu od wejścia do zapisu.
   - Ustal, gdzie mieszka reguła, którą zmieniasz.
4. **Kontrola danych.** Sprawdź issue według `definition-of-ready.md`:
   - kryterium „gotowe gdy”, które da się sprawdzić testem albo komendą;
   - dla błędu: objaw, dane, które go pokazują, i kroki odtworzenia albo powód, dla którego odtworzenie jest niemożliwe;
   - zakres: pliki i warstwy, których zmiana dotyczy;
   - zależności od innych issue i ich stan.

   Brakującą etykietę dopisujesz sam. To nie jest powód do pytania.

   Issue sprzeczne, niewykonalne, za duże na jeden PR albo łamie regułę krytyczną projektu? Taki problem trafia do pytań z kroku 6.
5. **Decyzje.** Wypisz wybory, których issue nie rozstrzyga. Definicja: sekcja „Co jest decyzją”.
   - **Strażnik nr 1.** Decyzja z sekcji „Decyzje opiekuna” w `project.md` zawsze trafia do pytań.
     Dotyczy to także decyzji, na którą dokumentacja podpowiada odpowiedź.
6. **Pytania.** Postępowanie zależy od trybu.

   **Tryb domyślny: rozmowa.** Prowadzisz ją skillem z wiersza „Specyfikacja z opiekunem” w sekcji „Dobór skilli” w `project.md`.
   - Na starcie przekaż temu skillowi zasady z tej listy.
   - Pytania idą po jednym. Każde ma formę z sekcji „Pytania do operatora” w `project.md`.
   - Proponujesz 2-3 podejścia z rekomendacją. Operator wybiera.
   - **Strażnik nr 1.** Każda decyzja z sekcji „Decyzje opiekuna” jest omówiona w rozmowie.
   - Skill rozmowy nie zapisuje własnego pliku, nie commituje i nie przechodzi do pisania planu.
   - Wynik rozmowy trafia do kroku 7.
   - Bez tego skilla prowadzisz rozmowę sam według tej listy.

   Rozmowa pokazuje, że issue jest za duże na jeden PR? Zaproponuj podział. Dopiero po zgodzie operatora:
   - załóż issue dla pozostałych części: skill `ba-github-issues create`;
   - zostaw w bieżącym issue komentarz z podziałem: skill `ba-github-issues comment <n> <treść>`;
   - pracuj dalej nad pierwszą częścią jako zakresem bieżącego issue.

   Podział wychodzi dopiero po zapisaniu specyfikacji? Zawęź zakres w tym samym pliku i zapytaj o akceptację ponownie.

   **Tryb `--auto`: jeden zestaw pytań.** Jest brak z kroku 4 albo decyzja z kroku 5? Zakończ turę jednym zestawem pytań.
   - Formę pytań podaje sekcja „Pytania do operatora” w `project.md`.
   - Każdy brak i każda decyzja dostaje opcje do wyboru i rekomendację.
   - Nie zgaduj brakujących danych.
   - Bez odpowiedzi nie powstaje specyfikacja.
   - Po odpowiedzi wróć do kroków 4-5 dla tego, czego dotyczyła. Nowy brak albo nowa decyzja daje kolejny zestaw pytań.

   Issue kompletne i bez decyzji przechodzi do kroku 7 bez pytań.
7. **Specyfikacja.** Napisz ją z `spec-template.md`.
   - Funkcjonalność i zmiana zachowania dostają wersję pełną. Błąd dostaje wersję krótką.
   - Plik: `.ai/specs/YYYY-MM-DD-slug.md`. Datę bierzesz z `date +%F`. Slug to krótki opis po angielsku w kebab-case. Nie kończy się na `-plan`.
   - Specyfikacja ma linię `Issue: #<n>`.
   - Odpowiedzi operatora i wybrane podejście trafiają do treści. Odrzucona alternatywa też, z powodem.
   - Tryb domyślny: po zapisaniu specyfikacji zapytaj operatora o akceptację. Opcje: „akceptuję” albo „poprawki”. Forma jak w sekcji „Pytania do operatora”.
   - „Poprawki” wracają do rozmowy z kroku 6. Bez akceptacji nie powstaje plan.
   - Tryb `--auto` nie pyta o akceptację.
8. **Plan.** Napisz go sam z `plan-template.md`, obok specyfikacji. Plan nie czeka na akceptację operatora w żadnym trybie.
   - Plik: `.ai/specs/YYYY-MM-DD-slug-plan.md`, z tą samą datą i slugiem.
   - Plan ma linię `Issue: #<n>` i link do specyfikacji.
   - Każde zadanie ma pliki, test przed kodem, komendę z oczekiwanym wynikiem i treść commita.
   - Skille i agentów w zadaniach dobierasz według sekcji „Dobór skilli” w `project.md`.
9. **Komentarz z planem.** Skill `ba-github-issues comment <n> <treść>`. Komentarz nie wymaga gałęzi.
   Treść ma do 10 linii:
   - przeczytane dokumenty;
   - odpowiedzi operatora i źródła, na które się powołałeś;
   - wybrane podejście i odrzucona alternatywa;
   - pasujące wiersze z sekcji „Dobór skilli”;
   - ścieżki specyfikacji i planu.

Specyfikacja i plan powstają zawsze, także dla błędu. Jakość jest ważniejsza niż koszt.

Plan (krok 8) i tryb `--auto` pracują bez operatora. Nie wołają skilli, które kończą się pytaniami do człowieka. Ich listę podaje sekcja „Dobór skilli” w `project.md`.

## Co jest decyzją

Decyzja to wybór, którego issue nie rozstrzyga i który zmienia jedno z poniższych:

- zachowanie widoczne dla użytkownika;
- wynik obliczeń, które system pokazuje albo zapisuje;
- schemat danych;
- zakres zadania.

Wybór rozstrzygnięty przez dokumentację albo najbliższy istniejący kod nie jest decyzją. Stosujesz źródło i wpisujesz je do specyfikacji. Wyjątkiem jest decyzja opiekuna.

Decyzja opiekuna to decyzja z listy w sekcji „Decyzje opiekuna” w `project.md`. Agent nie podejmuje jej sam.

Szczegół implementacji bez wpływu na zachowanie rozstrzygasz sam. Przykład: nazwa funkcji albo układ testu.

## Istniejąca specyfikacja

W `.ai/specs/` leży już specyfikacja albo plan z linią issue? Uzupełnij je zamiast pisać drugą parę.

- Linia issue to `Issue: #<n>` albo `**Issue:** #<n>`. Po numerze nie stoi cyfra. Dla `#101` linia `Issue: #1018` nie pasuje.
- Plan to plik z końcówką `-plan.md` i linią `Specyfikacja:` z linkiem do jego specyfikacji. Specyfikacja to drugi plik pary.
- Pomijasz katalogi `implemented/` i `archive/`.
- Brakujący plik z pary dopisujesz obok istniejącego, z tą samą datą i slugiem.
- Treść sprawdzasz krokami 3-6 jak nową. Nowy brak albo decyzja trafia do pytań.
- Więcej niż jedna para dla `#<n>` daje pytanie do operatora, którą wziąć.
