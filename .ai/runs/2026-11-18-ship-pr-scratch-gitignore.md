# Dziennik: katalog roboczy `ba-ship-pr` w `.ai/scratch/`

Issue: #7

Plan: [`.ai/specs/implemented/2026-11-18-ship-pr-scratch-gitignore-plan.md`](../specs/implemented/2026-11-18-ship-pr-scratch-gitignore-plan.md)

## Postęp

- [x] Task 1: wpis `.ai/scratch/` w `.gitignore`. Commit `5bd16fa`.
- [x] Task 2: `ba-ship-pr` zapisuje do `.ai/scratch/reviews/`. Commit `a1f742f`.
- [x] Task 3: `ba-setup` dopisuje `.ai/scratch/` do `.gitignore`, `README.md`.

## Wybory

- **Zadania wykonane w głównej sesji, bez podagenta na zadanie.** Każde zadanie to kilka linii tekstu w skillu i test. Recenzję całej gałęzi robi pętla review w `ba-ship-pr`.
- **`import re` dopiero w Task 3.** Plan dawał go w Task 1. Ruff zgłosiłby nieużywany import w commicie Task 1.
- **Test `git check-ignore` przez `shutil.which("git")`, `noqa: S603` i `timeout=30`.** Ruff zgłosił `S607` na gołym `"git"`. Wzorzec z `tests/support/tracked_files.py`.
- **Opis `description` w `ba-setup` wspomina `.ai/scratch/`.** Plan tego nie wymieniał. Opis wylicza wszystkie skutki skilla, więc nowy skutek też.
- **Autor commitów z historii repo i konta `gh`.** Środowisko nie ma `user.name`. Ustawione tylko dla polecenia `git -c`.
- **Cofnięty lokalny commit autosave narzędzia.** Commit `cezar autosave (run finalize)` z samą specyfikacją. Nie był wypchnięty. Cofnięty `git reset --soft`, specyfikacja weszła do commita Task 1.

## Weryfikacja

- Bramka jakości: `uv sync --locked`, `ruff check`, `ruff format --check` zielone. `pytest`: **96 passed**.
- Weryfikacja mutacyjna `tests/test_scratch_dir.py`. Każda mutacja wywala 1 test:
  - `.gitignore` bez linii `.ai/scratch/`;
  - `ba-ship-pr` z `mkdir -p .claude/scratch/reviews`;
  - `ba-setup` bez nagłówka `## Wpis w .gitignore`;
  - krok 4 `ba-setup` bez odwołania do § Wpis w .gitignore;
  - `README.md` bez zdania o `.ai/scratch/`.
- Druga droga: blok 1.0 z `ba-ship-pr` w świeżym repo z `mktemp -d`.
  - Bez wpisu `git check-ignore -q .ai/scratch/x` daje kod 1, z wpisem kod 0.
  - Snapshot i indeks powstają w `.ai/scratch/reviews/`.
  - `git add -A` zabiera tylko `.gitignore` i `app.txt`, bez snapshotu.

## Lokalne review (`ba-ship-pr`, Faza 2)

- Skill użyty z tej gałęzi: snapshot i raporty w `.ai/scratch/reviews/`. Zainstalowana kopia skilla ma jeszcze `.claude/scratch/`.
- Runda 1: 3 audytorzy i `code-review:challenger`. Bez `code-review:cross-verifier`: zakres to 8 plików tekstu.
  - Poprawione: zdanie w README o ponownym `ba-setup`; „Wejście” w `ba-setup`; testy kroków 5 i 8 oraz raportu.
  - Poprawione LOW: źródło reguły w teście (`check-ignore -v`), fraza o końcowym znaku nowej linii.
  - Odrzucone przez challengera: test zgodności ścieżki między skillami, test README.
- Runda 2: `ba-setup` sprawdza źródło reguły. Reguła globalna i `.git/info/exclude` się nie liczą. Test frazy o nowej linii. Podmiot zdania w README.
- Runda 3: reguła z `!` dawała fałszywe „wpis już jest”. Poprawione: `git check-ignore -q` przed `-v`.
- Każda poprawka ma mutację, która wywala test. Blok z § Wpis w .gitignore sprawdzony w świeżym repo: brak reguły, reguła globalna, `info/exclude`, nieśledzony `.gitignore`, reguła z `!` dają „dopisz”; śledzony `.gitignore` z wpisem daje „wpis już jest”.
- Pominięte LOW: ta sama informacja w „Wejście” i na końcu § Wpis w .gitignore.
- Runda 4 na prośbę operatora. Znalazła: brak testu uruchamiającego blok (HIGH), fałszywe „wpis już jest” dla niezacommitowanej linii (MEDIUM), regułę z `!` w teście repo (LOW).
  - Decyzja według 2.6, opcja prostsza: `ba-setup` sprawdza dosłowną linię `.ai/scratch/` w `.gitignore` (`grep -qxF`). Wykrywanie przez `git check-ignore` odrzucone. Zdublowana reguła przy szerszym `.ai/` nic nie psuje.
  - Krok 8 zabiera `.gitignore`, gdy plik różni się od `HEAD`. Łapie to linię dopisaną wcześniej bez commita.
  - Test uruchamia blok z sekcji na 6 wariantach `.gitignore`. Test repo sprawdza linię w `.gitignore` i `git check-ignore -q`.
  - Mutacje: `grep` bez `-x`, szersza reguła, powrót do `check-ignore`, brak `git diff --quiet HEAD`, krok 8 bez `.gitignore`. Każda wywala test.
- Bramka po rundzie 4: ruff zielony, pytest **102 passed**.
- Po rundzie 4 bez kolejnego review lokalnego. Uproszczenie usuwa klasy przypadków z rund 2-4. Review człowieka w PR obejmie nową wersję.
