# Definition of Done (DoD)

> Pojedyncza checklista warunków, po których zadanie w repozytorium jest **UKOŃCZONE**. Trzy typy zadań — **FEATURE**, **BUG**, **GENERAL** — odpowiadają typom issue (`feat` / `bug` / brak typu). DoD to brama **wyjściowa** zadania. Bramą wejściową jest [`definition-of-ready.md`](definition-of-ready.md).

---

## Spis treści

1. [Wspólne kryteria](#1-wspólne-kryteria)
2. [Quality Gate](#2-quality-gate)
3. [Reguły krytyczne](#3-reguły-krytyczne)
4. [Per typ zadania](#4-per-typ-zadania) — FEATURE / BUG / GENERAL, [usuwanie kodu](#44-usuwanie-kodu)
5. [Co NIE jest częścią DoD](#5-co-nie-jest-częścią-dod)
6. [Hooki sesyjne](#6-hooki-sesyjne)

---

## 1. Wspólne kryteria

Obowiązują **każde** zadanie, niezależnie od typu.

| Wymóg | Szczegóły |
|---|---|
| **Quality Gate zielony** | Komendy z [`project.md` § Bramka jakości](project.md#bramka-jakości) |
| **Druga, niezależna droga weryfikacji** | Wynik sprawdzasz dwa razy, dwiema różnymi drogami. Zielony test to nie dowód. Pary dróg stoją niżej |
| **Testy zmienionej logiki** | Zmieniona logika ma test, który pada bez tej zmiany |
| **Dokumentacja zsynchronizowana** | Zmiana zachowania albo struktury aktualizuje dokumentację **w tym samym zadaniu**. {Mapa dokumentacji, na przykład `docs/README.md`, i skill synchronizacji, gdy repo go ma} |
| **Brak sekretów w kodzie** | Hasło, klucz ani token nie trafiają do repozytorium. Szczegóły w § 3 |
| **Opis PR-a kompletny** | Sekcje opisu z [`pull-request.md` § Opis PR-a](pull-request.md#opis-pr-a) nie są puste |
| **Wiedza zapisana w `.ai/`** | Poprawka z regułą na przyszłość daje lekcję w `.ai/lessons/`. Zrobiona specyfikacja idzie do `.ai/specs/implemented/` |
| **Rozwiązanie proste** | Najmniejsza zmiana, która spełnia zadanie. Bez kodu na zapas |
| **Brak nieintencjonalnej regresji** | Testy, których kontraktu zadanie nie zmienia, przechodzą bez zmiany asercji. FEATURE zmieniający kontrakt aktualizuje testy: § 4.1. GENERAL zmieniający asercje to nie GENERAL: § 4.3 |
| **Usunięty kod bez śladu** | Zadanie, które usuwa kod, przechodzi checklistę z [§ 4.4](#44-usuwanie-kodu) |

### Druga droga weryfikacji

Druga droga musi być **niezależna** od pierwszej. To samo sprawdzenie innym poleceniem nie jest drugą drogą.

| Pierwsza droga | Druga droga |
|---|---|
| Test jednostkowy | Weryfikacja mutacyjna: cofnij poprawkę, test ma paść |
| Pomiar na danych | Prześledzenie kodu, który je produkuje |
| Twierdzenie o zachowaniu | Uruchomienie na danych przygotowanych pod ten przypadek |
| Liczba z raportu | Przeliczenie z innego źródła |

Dwie drogi dają różne wyniki? To jest znalezisko. Ustal, która kłamie, zanim pójdziesz dalej.

---

## 2. Quality Gate

Komendy bramki stoją w [`project.md` § Bramka jakości](project.md#bramka-jakości). {Workflow CI, który uruchamia te same checki. Usuń zdanie, gdy repo nie ma CI.}

{Warunki per obszar zmiany z wywiadu. Każdy to podsekcja `### Gdy zmiana dotyka <obszar>`, na przykład frontend, migracje bazy, zależności. Usuń, gdy brak.}

---

## 3. Reguły krytyczne

Naruszenie którejkolwiek reguły znaczy: zadanie **nie jest** ukończone, nawet przy zielonej bramce.

### Brak sekretów w kodzie

- Hasło, klucz API ani token nie trafiają do kodu, testów ani dokumentacji.
- Sekret czyta się ze zmiennej środowiskowej albo z menedżera sekretów.
- Sekret w historii gita to incydent. Trzeba go unieważnić, samo usunięcie z kodu nie wystarcza.

{Reguły krytyczne projektu z wywiadu. Każda to podsekcja `### <nazwa>` z krótkimi punktami, na przykład integralność danych albo bezpieczeństwo bazy. Usuń, gdy brak.}

---

## 4. Per typ zadania

Każde zadanie ma **dokładnie jeden** typ. Typ zmiany wynika z etykiety typu issue ([`labels.md`](labels.md#grupy)).

### 4.1 FEATURE

Nowa funkcjonalność widoczna dla użytkownika albo nowy mechanizm wewnętrzny.

- Testy pokrywają co najmniej **główną ścieżkę i jeden przypadek brzegowy**.
- Zmiana w interfejsie jest sprawdzona **w przeglądarce**, nie tylko przez linter i testy.
- Dokumentacja odpowiada zakresowi zmiany: {mapa „typ zmiany → plik dokumentacji” z wywiadu}.

### 4.2 BUG

Naprawa istniejącej wadliwej logiki.

- **Test regresyjny** pada przed poprawką i przechodzi po niej. Brak testu wymaga uzasadnienia w opisie PR-a.
- **Test pisany po poprawce** sprawdzasz mutacyjnie: cofnij poprawkę, test ma paść, przywróć poprawkę. Zielony test nie dowodzi niczego, dopóki nie widziałeś go na czerwono.
- Opis PR-a mówi o **pierwotnym objawie**, nie tylko o diffie.
- Wniosek przydatny w innym zadaniu trafia jako lekcja do `.ai/lessons/`.
- Błąd zepsuł zapisane dane? Opis PR-a mówi, czy trzeba je poprawić po wdrożeniu.

### 4.3 GENERAL

Wszystko poza nową funkcją i naprawą błędu: porządkowanie kodu, konfiguracja, zależności, testy, dokumentacja, konfiguracja agenta.

- **Brak zmiany kontraktu publicznego ani zachowania widocznego dla użytkownika.** Istniejące testy przechodzą bez zmiany asercji.
  - Test wymaga zmiany logiki? To nie GENERAL, tylko FEATURE albo BUG.
- Porządkowanie kodu tylko na **wyraźne polecenie** użytkownika. Nigdy „przy okazji” innego zadania.
- Nowy dokument jest podlinkowany z mapy dokumentacji.
- Trwała dokumentacja nie linkuje do plików roboczych, na przykład `.ai/runs/`. Uzasadnienie wpisujesz wprost, w 1–2 zdaniach.

### 4.4 Usuwanie kodu

Usunięty kod nie zostawia śladu nigdzie w repozytorium.

Checklista obowiązuje przy każdym usuwaniu, niezależnie od typu zadania.

**Kod tymczasowy dostaje osobne pliki już przy dodawaniu.** Usunięcie to wtedy usunięcie plików i jednego wpisu, który je włącza.

**Wyszukaj nazwy.** Każdą nazwę usuwanego kodu szukaj w {katalogi repo do przeszukania, na przykład kod, testy, skrypty, workflowy CI, dokumentacja}:

- ścieżki tras, nazwy endpointów i modułów;
- modele, schematy i zmienne środowiskowe;
- parametry i flagi, które obsługiwały tylko usuwany kod;
- nazwy fixture'ów i helperów testowych.

**Konsumenci po usunięciu.** Wyszukiwanie nie łapie kodu, który stracił ostatniego użytkownika.

- Helper, którego jedynym konsumentem był usuwany kod, znika razem z nim.
- Sprawdź też konsumentów tego helpera. Usunięcie bywa łańcuchem kilku funkcji.
- Parametr, którego nie przekazuje już żaden wywołujący, znika.

**Usuwany test.** Asercja, której nie ma w żadnym innym teście, przechodzi do testu, który zostaje.

---

## 5. Co NIE jest częścią DoD

Granice tego dokumentu chronią checklistę przed rozrostem.

- **Commit, push, PR**: tylko na gałęzi roboczej, nigdy na gałęzi głównej. Brak commita nie blokuje uznania zadania za skończone.
- **Review kodu**: osobny proces, nie warunek DoD. Poprawki po review idą na tę samą gałąź i do tego samego PR-a.
- **Wdrożenie**: DoD kończy się na zielonej bramce jakości.
- **Pomiar wydajności**: tylko gdy zadanie wprost dotyczy wydajności.
- **Stan zadania w GitHub Issues**: opisuje go skill `ba-github-issues`, nie DoD.

---

## 6. Hooki sesyjne

{Hooki agenta zarejestrowane w repo: nazwa, zdarzenie, co robi. Hook wspiera DoD, ale go nie zastępuje. Usuń treść, gdy repo nie ma hooków.}
