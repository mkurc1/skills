# Katalog roboczy `ba-ship-pr` w `.ai/scratch/`, ignorowany przez `.gitignore`

Issue: #7

## Cel

`ba-ship-pr` zapisuje snapshot i raporty review w `.claude/scratch/reviews/`. Ten katalog nie jest ignorowany w tym repo ani w obcych repo. Snapshot z całym diffem gałęzi może wtedy wejść do commita albo PR-a.

Po zmianie katalog roboczy to `.ai/scratch/`. Ścieżka nie zależy od narzędzia agenta. `.gitignore` tego repo ignoruje `.ai/scratch/`. `ba-setup` dopisuje ten wpis do `.gitignore` obcego repo.

## Zakres

- `skills/ba-ship-pr/SKILL.md`: każdy zapis do `.claude/scratch/reviews/` idzie do `.ai/scratch/reviews/`.
  - Krok 1.0: `mkdir`, ścieżka snapshotu, indeks `pre-ship-pr-index.txt`.
  - § 2.7 Artefakty: miejsce zapisu raportów.
  - Faza 3: zdanie o miejscu raportów z Fazy 2.
- `skills/ba-ship-pr/SKILL.md` § 2.7: zdanie „Katalog jest w `.gitignore`” podaje, że wpis dodaje `ba-setup`.
- `skills/ba-setup/SKILL.md`: nowa sekcja `## Wpis w .gitignore` i odwołanie z kroków 4 i 5.
- `.gitignore` tego repo: wpis `.ai/scratch/`.
- `README.md`: wiersz `ba-setup` mówi o wpisie w `.gitignore`.
- Testy kontraktu w `tests/`.

### Poza zakresem

- Inne wzmianki o `.claude/` w `ba-ship-pr`: `:240`, `:257`, `:421`, `:437`. Nie dotyczą miejsca zapisu.
- `ba-setup/references/interview.md`: czyta `.claude/skills/` i `.claude/settings.json` obok innych narzędzi. To odczyt, nie zapis.
- Przenoszenie starych plików z `.claude/scratch/` w obcych repo. Katalog jest efemeryczny.

## Projekt

### Decyzje operatora

- `ba-ship-pr` nie sprawdza, czy katalog jest ignorowany. Nie zakłada pliku `.gitignore` ani wpisu w `.git/info/exclude`.
- Rozwiązanie ma być niezależne od dostawcy narzędzia agenta. Dlatego ścieżka przechodzi z `.claude/scratch/` do `.ai/scratch/`.
- Wpis w `.gitignore` obcego repo dodaje `ba-setup`.

### Odrzucone podejścia

- **Plik `.claude/scratch/.gitignore` z `*`, zakładany przez `ba-ship-pr`.** Operator nie chce, żeby `ba-ship-pr` tego pilnował. Ścieżka zostaje związana z Claude.
- **Wpis w `.git/info/exclude` z `ba-ship-pr`.** Te same powody. Wpis jest też niewidoczny dla użytkownika.
- **Tylko wpis w `.gitignore` tego repo.** Obce repo zostaje bez ochrony.

### Gdzie mieszka reguła

- Ścieżka katalogu roboczego: `skills/ba-ship-pr/SKILL.md`.
- Wpis w `.gitignore` obcego repo: `skills/ba-setup/SKILL.md` § Wpis w .gitignore.

### `ba-setup` § Wpis w .gitignore

1. Sprawdź dosłowną linię: `grep -qxF '.ai/scratch/' .gitignore`.
   - Linia jest: nic nie dopisujesz. Raport mówi „wpis już jest”.
   - Szersza reguła (`.ai/`), globalny plik ignorowania i `.git/info/exclude` się nie liczą. Zdublowana reguła nic nie psuje.
2. Brak linii: przygotuj linię `.ai/scratch/` na końcu `.gitignore`. Brak pliku: zakładasz go z tą linią. Plik bez końcowego znaku nowej linii najpierw go dostaje.
3. Podgląd z kroku 5 pokazuje zmianę `.gitignore` razem z plikami `.ai/config/`. Zapis idzie po tej samej akceptacji.
4. Commit z kroku 8 zabiera `.gitignore`, gdy plik różni się od `HEAD`. Dotyczy to też linii dopisanej wcześniej bez commita.

Wykrywanie przez `git check-ignore` odrzucone w review (rundy 2-4). Łapało regułę globalną, `.git/info/exclude`, regułę z `!` i niezacommitowany `.gitignore`. Dosłowna linia jest prostsza i nie ma tych przypadków.

Kroki `ba-setup` zachowują numerację. Wpis przygotowuje krok 4, pokazuje krok 5. Ponowne uruchomienie `ba-setup` w repo z kompletną konfiguracją też dopisuje brakujący wpis.

Raport końcowy `ba-setup` mówi, czy wpis dopisano, czy już był.

## Plan

1. Testy kontraktu: najpierw padają na obecnym stanie.
2. `.gitignore`: wpis `.ai/scratch/`. Sprawdzenie: `git check-ignore .ai/scratch/reviews/x.patch` zwraca ścieżkę.
3. `ba-ship-pr`: ścieżki `.ai/scratch/reviews/`. Sprawdzenie: test.
4. `ba-setup`: sekcja i odwołania w krokach. Sprawdzenie: test.
5. `README.md`. Bramka jakości z `project.md`.

## Gotowe gdy

- `git check-ignore .ai/scratch/reviews/x.patch` w tym repo zwraca ścieżkę.
- `grep -n ".claude/scratch" skills/` nie daje trafień.
- Test pilnuje, że `.gitignore` tego repo ignoruje `.ai/scratch/`.
- Test pilnuje, że `ba-ship-pr` zapisuje do `.ai/scratch/reviews/` i nie zapisuje do `.claude/scratch/`.
- Test pilnuje, że `ba-setup` ma sekcję `## Wpis w .gitignore` z `.ai/scratch/`, a krok 4 do niej odsyła. Test uruchamia blok sprawdzenia na wariantach `.gitignore`.
- Bramka jakości z `project.md` przechodzi.

## Ryzyka i otwarte pytania

- Repo skonfigurowane przed tą zmianą nie ma wpisu. Pomaga ponowne uruchomienie `ba-setup`. `README.md` to mówi.
- `.gitignore` obcego repo może ignorować całe `.ai/`. `ba-setup` i tak dopisze `.ai/scratch/`. Zdublowana reguła nic nie psuje.
