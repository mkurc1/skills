# Definition of Ready (DoR)

> Pojedyncza checklista warunków, po których zadanie w GitHub Issues jest **GOTOWE DO PODJĘCIA**. Trzy typy — **FEATURE**, **BUG**, **GENERAL** — odpowiadają etykietom issue (`feat` / `bug` / brak typu). DoR to brama **wejściowa** zadania. Bramą wyjściową jest [`definition-of-done.md`](definition-of-done.md).

---

## Spis treści

1. [Rdzeń MUST](#1-rdzeń-must) — warunki twarde, wspólne dla wszystkich typów
2. [Per typ zadania](#2-per-typ-zadania) — rekomendacje dla FEATURE / BUG / GENERAL
3. [Sygnały „issue nie jest gotowy"](#3-sygnały-issue-nie-jest-gotowy)
4. [Co NIE jest częścią DoR](#4-co-nie-jest-częścią-dor)

---

## 1. Rdzeń MUST

Obowiązuje **każde** issue, niezależnie od typu. Każdy punkt to warunek konieczny. Brak spełnienia znaczy: issue wymaga uzupełnienia, nie startu pracy.

Łańcuchy `ba-fix-issue` i `ba-auto-fix-issue` też wymagają gotowego issue. Sprawdza je `ba-github-issues start` na początku łańcucha. Otwarte decyzje projektowe rozstrzyga potem `ba-plan`. Niegotowe issue uzupełnia rozmową skill `ba-refine-issue`.

| Wymóg | Szczegóły |
|---|---|
| **Etykiety klasyfikacyjne** | Etykiety priorytetu i typu według reguł z [`labels.md`](labels.md#reguły). Typ wyznacza sekcję w § 2: FEATURE, BUG albo GENERAL |
| **Tytuł w języku projektu** | Język podaje [`project.md`](project.md#język). Tytuł mówi co, nie jak. Zalecane do 70 znaków. Bez emoji i bez prefiksów typu `[BUG]`, bo typ jest w etykietach |
| **Treść z kontekstem** | Szablon: [`issue-template.md`](issue-template.md). 1–3 zdania, **dlaczego** zadanie powstaje: problem, potrzeba albo obserwacja. Do tego obserwowalny stan końcowy („gotowe, gdy…”). „Zrób to lepiej” albo sam diff to nie kontekst |
| **Brak konfliktu z regułami krytycznymi DoD § 3** | Reguły w skrócie stoją niżej |
| **Zakres mieści się w jednym PR** | Zakres na więcej niż jeden PR albo kilka niezależnych zmian? Rozbij issue na mniejsze **przed startem**. Jeden PR to jedno issue |
| **Zależności wymienione** | Zadanie blokuje inne albo czeka na inne? Treść mówi „blokuje #X” albo „zależy od #Y”. Decyzja architektoniczna wymaga linku do zapisu decyzji (ADR) albo adnotacji „wymaga ADR” |

### Reguły krytyczne DoD § 3 w skrócie

{Reguły krytyczne projektu z wywiadu, po jednym punkcie: sama nazwa z linkiem do podsekcji w [`definition-of-done.md` § 3](definition-of-done.md#3-reguły-krytyczne). Treść reguły stoi tylko w DoD. Usuń listę, gdy projekt ich nie ma.}

Zadanie, które z natury dotyka tych obszarów, potrzebuje w treści uzasadnienia i planu obejścia.

---

## 2. Per typ zadania

Listy poniżej to **rekomendacje**, nie MUST. Podnoszą jakość issue danego typu. Małe zadanie może pominąć większość, ale § 1 obowiązuje zawsze.

### 2.1 FEATURE

Nowa funkcjonalność widoczna dla użytkownika albo nowy mechanizm wewnętrzny.

- **Grupa docelowa**: kto korzysta z funkcji, na przykład użytkownik, administrator albo zadanie automatyczne.
- **Dotknięte warstwy**: {warstwy systemu z wywiadu, na przykład API, interfejs, baza}. Pomagają ocenić zakres i dokumentację do aktualizacji.
- **Kryterium akceptacji do sprawdzenia**: „endpoint zwraca X dla Y”, „strona pokazuje Z w stanie W”. Nie „działa lepiej”.
- **Link do wymagań**: {miejsce opisu wymagań produktu w repo; usuń, gdy brak}.
- **Powiązany zapis decyzji (ADR)**: zmiana granic modułów albo kontraktu między modułami linkuje ADR. Bez niego treść mówi „wymaga nowego ADR przed startem”.

### 2.2 BUG

Naprawa istniejącej wadliwej logiki.

- **Obserwowany objaw**: skąd zgłoszenie (interfejs, log, test, ręczne sprawdzenie) i co dokładnie widać.
- **Kroki odtworzenia** albo minimalny przykład. Bez odtworzenia treść mówi dlaczego, na przykład „wyścig, tylko pod obciążeniem”.
- **Środowisko**: produkcja, środowisko testowe albo lokalne. Wersja kodu, gdy ma znaczenie.
- **Oczekiwane i obserwowane zachowanie**: obie strony jednoznacznie.
- **Wpływ na zapisane dane**: czy błąd zepsuł dane, które trzeba poprawić po naprawie.

### 2.3 GENERAL

Porządkowanie kodu, konfiguracja, zależności, testy, dokumentacja, zmiany w konfiguracji agenta.

- **Uzasadnienie „dlaczego teraz”**: porządkowanie kodu tylko na wyraźne polecenie. „Przy okazji” nie jest uzasadnieniem.
- **Brak zmiany kontraktu publicznego**: istniejące testy przechodzą bez zmiany asercji. Test wymaga zmiany? To FEATURE albo BUG, nie GENERAL.
- **Zmiana schematu bazy**: jaka semantyka się zmienia i czy dane wymagają przeniesienia.
- **Zmiana w dokumentacji**: usuwasz albo przenosisz sekcję? Najpierw wyszukaj odwołania i wypisz trafienia w treści.

---

## 3. Sygnały „issue nie jest gotowy"

Gdy widzisz te sygnały przed startem pracy, zostaw komentarz z brakiem i nie podejmuj zadania.

- Tytuł abstrakcyjny: „ulepsz system”, „popraw UI”, „refaktor backendu”.
- Treść bez „dlaczego”: sam opis tego, co zrobić, bez problemu, który to rozwiązuje.
- Kilka niezależnych zmian w jednym issue. Każda mogłaby być osobnym PR-em.
- Konflikt z regułami krytycznymi DoD § 3 bez planu obejścia w treści.
- Decyzja architektoniczna ukryta w issue, bez zapisu decyzji (ADR).
- Etykiety priorytetu albo typu łamią reguły z [`labels.md`](labels.md#reguły).
- „TODO”, „Naprawić” albo „Zobaczyć” jako tytuł.

---

## 4. Co NIE jest częścią DoR

Granice tego dokumentu chronią checklistę przed rozrostem.

- **Estymacja czasu i wielkości**: DoR jej nie wymaga.
- **Przydzielenie osoby (assignee)**: dzieje się przy starcie pracy (`ba-github-issues start`), nie przy sprawdzaniu DoR.
- **Ścieżka implementacji i projekt techniczny**: to praca po starcie. DoR mówi *co* i *dlaczego*, nie *jak*.
- **Decyzja, czy zadanie w ogóle zrobimy**: to zarządzanie backlogiem. DoR mówi tylko, czy issue jest gotowe do podjęcia.
- **Review, bramka jakości, commit, PR**: to wynik wykonania. Należą do DoD.

Sprawdzenie DoR odbywa się przy starcie pracy (`ba-github-issues start`).
Issue bez etykiety stanu `in-progress` to kandydat w backlogu. Nazwę etykiety podaje [`statuses.md`](statuses.md#stany).
