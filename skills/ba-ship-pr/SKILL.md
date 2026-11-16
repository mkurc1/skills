---
name: ba-ship-pr
description: Use ONLY when the user explicitly runs /ba-ship-pr (or directly asks for this PR-finalization workflow), or as the shipping step of the user-invoked ba-auto-fix-issue or ba-fix-issue chain — NEVER auto-invoke from repo state such as "branch looks ready" or "tests are green". It runs the Quality Gate, then a local review loop (code-review plugin auditors scoped to the branch diff, up to 3 rounds, fixes applied automatically), cleans up review artifacts (docs/reviews, docs/superpowers), commits + pushes, opens a PR, resolves merge conflicts with main, then waits for every check on the pull request through ba-wait-checks, critically vets PR feedback and applies only the real fixes. Optionally pass a PR number to re-check its feedback/CI. Running it is the user's explicit consent for git commit/push and PR creation; do not trigger it yourself.
---

# /ba-ship-pr — finalizacja gałęzi z review i krytyczna obsługa feedbacku

Wieloetapowy workflow zamykający code review. Wywołanie tego skilla (`/ba-ship-pr`) = **wyraźna zgoda** użytkownika na operacje gita (commit/push) i utworzenie PR-a (`gh pr create`) — nie pytaj o potwierdzenie.

## ⚠️ Tylko na jawne wywołanie użytkownika

Ten skill wykonuje `commit`, `push` i `gh pr create`. Uruchamiaj go **WYŁĄCZNIE** gdy użytkownik jawnie wpisał `/ba-ship-pr` lub wprost poprosił o ten workflow. **NIGDY nie wywołuj go autonomicznie** na podstawie wnioskowania w stylu „branch jest gotowy", „testy są zielone" czy „skończyłem funkcjonalność". To ciężki przebieg z pętlą review i odpytywaniem PR-a, więc o jego starcie decyduje użytkownik. Jeśli sam rozważasz użycie tego skilla — **STOP**: zaproponuj go użytkownikowi i czekaj na potwierdzenie, zamiast go odpalać.

Jedyny wyjątek: krok wysyłki łańcuchów **`ba-auto-fix-issue`** i **`ba-fix-issue`**. Użytkownik wywołał jeden z nich jawnie. Ta zgoda obejmuje `ba-ship-pr` i ma pierwszeństwo przed akapitem wyżej.

## Wywołanie

| Wywołanie | Co robi | Co zostawia |
|---|---|---|
| `/ba-ship-pr` | Kończy bieżącą gałąź: bramka, review, commit, push, PR | PR bieżącej gałęzi z zielonymi checkami |
| `/ba-ship-pr <pr_num>` | Sprawdza feedback i CI wskazanego PR-a | Zastosowane poprawki i stan PR-a |

Argument **`<pr_num>`** to numer PR-a do przeglądu feedbacku. Jeśli podany przy wywołaniu skilla, użyj go wszędzie tam, gdzie poniżej pada `<pr_num>` / „numer PR-a z argumentu". Jeśli brak — PR bieżącej gałęzi (`gh pr view --json number -q .number`).

Skill jest **idempotentny i ponownie wywoływalny** — przy każdym wywołaniu sprawdza stan gałęzi i PR-a, i kontynuuje od właściwej fazy. Faza zależy od stanu:

| Stan | Wykonywana faza |
|---|---|
| Niezacommitowane zmiany + brak PR-a dla gałęzi | Fazy 1 → 2 → 3 → 4 → 5 → 5.5 (jeśli konflikt) → Faza 6 (gate, pętla review, cleanup, commit, push, PR create, conflict resolve, feedback review + wynik sprawdzeń) |
| Niezacommitowane zmiany + istniejący PR dla gałęzi | Fazy 1 → 2 → 3 → 4 → 5.5 (jeśli konflikt) → Faza 6 (gate, pętla review, cleanup, commit, push, conflict resolve, feedback review + wynik sprawdzeń) |
| Brak niezacommitowanych zmian + istniejący PR | Faza 5.5 (jeśli konflikt) → Faza 6 (feedback review + wynik sprawdzeń) |
| PR z `mergeStateStatus` = DIRTY (albo BEHIND, gdy ruleset wymaga aktualnej gałęzi — patrz 5.5.1) | Faza 5.5 (merge z main + konflikt resolve) → Faza 6 |
| Czyste drzewo + commity ponad `main` + brak PR-a | Fazy 1 → 2 → 3 → 4 (commit tylko, gdy Faza 2 coś zmieniła) → 5 → 5.5 (jeśli konflikt) → Faza 6 |
| Czyste drzewo + brak commitów ponad `main` + brak PR-a | STOP — nic do zrobienia, zgłoś użytkownikowi |

Po każdym pushu skill czeka na wynik każdego sprawdzenia PR-a: skill `ba-wait-checks <pr_num>`. Stan sprawdzeń podajesz tylko z jego raportu. Nie kończysz tury z przewidywaniem w stylu „powinno być zielone”. Dalszy krok wybiera sekcja **6.6 Wynik sprawdzeń**.

## Konfiguracja

Na początku pracy przeczytaj te pliki z `.ai/config/`:

| Plik | Co daje |
|---|---|
| `project.md` | § Bramka jakości: komendy, warunki, auto-fix, narzędzie granic modułów |
| `pull-request.md` | gałąź główna, opis PR-a, dowód weryfikacji, werdykt review AI, merge, obszary wrażliwe, pliki blokad zależności, checki w CI |
| `labels.md` | prawdziwe nazwy etykiet PR-ów dla nazw logicznych |
| `code-review.md` | reguły projektu dla audytorów w Fazie 2 |

**Brak pliku** zatrzymuje skill. Podaj użytkownikowi nazwę brakującego pliku. Brakujące pliki generuje skill `ba-setup`.

Gałąź główna w tym skillu to gałąź z `pull-request.md` § „Gałąź główna”. Przykłady poleceń piszą ją jako `main`. Inną nazwę podstawiasz.

Etykiety skill wskazuje nazwą logiczną, na przykład `<etykieta zablokowanego PR-a>`. Prawdziwą nazwę bierzesz z `labels.md`.

---

## Faza 1 — Quality Gate (lokalnie, zanim wypchniemy)

### 1.0 Punkt odniesienia — PIERWSZA rzecz w całym skillu

Zanim cokolwiek dotknie plików, zapisz stan sprzed automatycznych edycji:

```bash
mkdir -p .claude/scratch/reviews
git fetch origin main -q                          # świeży origin/main, inaczej merge-base cofa się za daleko
base=$(git merge-base origin/main HEAD)
sha=$(git rev-parse --short HEAD)
snap=".claude/scratch/reviews/pre-ship-pr-$sha-$(date +%H%M%S).patch"
ita=$(git ls-files --others --exclude-standard)   # co było nieśledzone PRZED
git add -A -N                                     # intent-to-add: nowe pliki wejdą do diffa
test -e "$snap" || git diff --binary "$base" > "$snap"
# zdejmij znaczniki i-t-a — indeks musi wrócić do stanu sprzed tego bloku
[ -n "$ita" ] && printf '%s\n' "$ita" | tr '\n' '\0' | xargs -0 git rm --cached -q --
echo "$sha $base $snap" >> .claude/scratch/reviews/pre-ship-pr-index.txt
echo "punkt odniesienia: $snap (base $base)"
```

Cztery rzeczy, których ten blok pilnuje:

- **Idzie przed auto-fixem lintera poniżej.** Auto-fix lintera sam edytuje pliki i potrafi skasować import uznany za nieużywany. Checkpoint zrobiony po nim zapisałby już zmieniony stan.
- **`git add -A -N` wciąga pliki nieśledzone**, które Faza 2 też bierze do zakresu. Bez tego nowy plik nie ma z czego zostać odtworzony.
- **Znaczniki intent-to-add są zdejmowane od razu**, więc blok nie zostawia po sobie śladu w indeksie. Zostawione, psują `git stash push` („Entry not uptodate") i chowają pliki przed `git clean -fd`, a przy `git checkout -- .` ścinają nowy plik do zera bajtów. Zdejmujemy wyłącznie pliki z listy `ita` — `git reset` byłby zbyt szeroki i odstage'owałby to, co użytkownik świadomie przygotował przed wywołaniem skilla. Nazwy z **nową linią** w środku wymagałyby `git ls-files -z`; spacje `xargs -0` obsługuje.
- **Znacznik czasu w nazwie rozdziela kolejne wejścia.** Skill jest ponownie wywoływalny, a drugie wejście nie może zamazać kopii stanu sprzed pierwszego — to nazwa unikalna co do sekundy daje tę ochronę, nie `test -e`, który przy takiej nazwie prawie nigdy nie trafia. Guard zostaje jako zabezpieczenie przed dwoma wejściami w tej samej sekundzie. Trójka SHA↔base↔ścieżka dopisuje się do `pre-ship-pr-index.txt`, więc raport STOP zawsze wskaże właściwy snapshot.

Podawaj w **każdym** raporcie STOP z Fazy 1 i 2 obie wartości — `$sha` i `$base` — razem z procedurą odtworzenia. Sama ścieżka do pliku zostawia użytkownika bez instrukcji, co z nim zrobić, a bez `$base` musiałby przeliczać merge-base samodzielnie:

```bash
base=<base z raportu>; snap=<snapshot z raportu>
git checkout "$base" -- .                                    # cofa pliki śledzone
for f in $(git apply --summary "$snap" | awk '/create mode/{print $NF}'); do rm -f "$f"; done
git apply "$snap"                                            # odtwarza wszystko, w tym nowe pliki
```

Pętla `rm -f` nie jest zbędna. `git checkout "$base" -- .` nie tyka pliku, którego w bazie nie było, więc nowy plik zostaje w drzewie — choćby jako zero bajtów po nieudanej edycji. Wtedy `git apply` przerywa całość na `already exists in working directory` i nie odtwarza **niczego**. Sprawdzone: bez tej pętli plik zostaje pusty, a modyfikacje plików śledzonych też nie wracają. `git apply --3way` tu nie pomaga — nowego pliku nie ma w indeksie, więc trójstronne scalenie nie ma się o co oprzeć.

Obie wartości siedzą też w `pre-ship-pr-index.txt`, gdyby raport przepadł.

Snapshot jest liczony od `merge-base`, więc zawiera całą pracę gałęzi plus drzewo robocze. To backstop, nie minimalny diff — zacommitowane rzeczy i tak odzyskasz z reflogu.

### 1.1 Bramka

Uruchom bramkę jakości przed commitem, by nie wypychać zielonego CI tylko po to żeby było czerwone na zdalnym. Komendy stoją w `.ai/config/project.md` § „Bramka jakości”.

- Pierwszy blok podsekcji „Zawsze” uruchamiasz zawsze, komenda po komendzie.
- Pierwszy blok podsekcji z warunkiem uruchamiasz, gdy diff gałęzi dotyka katalogu z jej nazwy.
- Bloki „Auto-fix” uruchamiasz tylko według akapitu o auto-fixie niżej.

Narzędzie granic modułów z tej sekcji jest częścią bramki. Bez niego reguła o granicach z 2.6 nie ma czym zadziałać, a złamana granica wychodzi dopiero jako czerwony CI.

Czerwony krok: znajdź przyczynę, napraw ją i uruchom bramkę od nowa. Po 3 nieudanych próbach albo przy awarii infrastruktury (sieć, baza, zmienne środowiskowe) — STOP i raport. **Nie commituj** zielonego-z-czerwonym-output (popularny błąd).

Auto-fix to wyłącznie bloki „Auto-fix” z `project.md` § „Bramka jakości”. Nie próbuj „naprawiać" testów przez wyłączenie ich.

Gate idzie **przed** pętlą review, bo jest tani i wychwytuje oczywiste rzeczy, których nie warto wysyłać audytorom.

## Faza 2 — Lokalna pętla review (przed pushem)

Cel: dostać feedback review **od razu**, zamiast pushować i czekać 3–10 minut na run GitHub Actions, potem odpowiadać i czekać znowu.

Review na GitHubie zostaje bez zmian (Faza 6). Jest niezależnym, końcowym sprawdzeniem — startuje na czystym kontekście i widzi to, czego lokalna pętla nie zobaczy, bo pracuje w tej samej sesji z tymi samymi ślepymi plamami. Ta faza ma sprawić, że rund na GitHubie będzie mniej, nie że znikną.

Silnikiem jest plugin `code-review`. Nie piszemy własnego reviewera.

### 2.1 Zbierz zakres

```bash
git fetch origin main -q
base=$(git merge-base origin/main HEAD)
git diff --name-only "$base" | grep -vE '^docs/(reviews|superpowers)/'
git ls-files --others --exclude-standard | grep -vE '^docs/(reviews|superpowers)/'
git diff --stat "$base" | tail -1
```

Filtr na `docs/reviews/` i `docs/superpowers/` nie jest ozdobnikiem. Oba katalogi są nieśledzone i **nie są w `.gitignore`**, a sprzątanie stoi dopiero w Fazie 3. Bez filtru audytorzy dostaliby do oceny cudze raporty review — znalezisko na takim pliku zjadłoby rundę z limitu 3 i mogło zablokować push przez plik, który i tak zaraz kasujemy.

Filtr musi wisieć na **obu** komendach. Sekcja 1.0 zdejmuje znaczniki intent-to-add, więc pliki nieśledzone wracają do `git ls-files --others`, a `git diff --name-only` oddaje zmiany w plikach śledzonych — `diff` nigdy nie listuje nieśledzonych. Gdyby jednak 1.0 nie zdążyło się wykonać albo przerwało między `git add -A -N` a zdjęciem markerów, podział byłby odwrotny. Nie kasuj filtra z żadnej z komend jako „nadmiarowego".

Jeśli `git log --oneline "$base"..HEAD | wc -l` daje podejrzanie dużo commitów, gałąź prawdopodobnie wyszła z gałęzi zmergowanej squashem — wtedy `merge-base` cofa się za daleko i audytorzy dostaną cudzą, zmergowaną już pracę. Najpierw 5.5.3, dopiero potem pętla.

**Nie używaj `origin/main...HEAD`.** Trzykropek porównuje dwa commity i pomija drzewo robocze. Faza 2 biegnie przed commitem z Fazy 4, więc trzykropek pokazałby wszystko poza tym, co właśnie wysyłasz — a przy gałęzi bez commitów zwróciłby pustkę i cicho wyłączył całą fazę.

Punkt odniesienia sprzed autonomicznych edycji powstał już w 1.0 — nie rób go tutaj drugi raz.

Pusty zakres (żaden z trzech powyższych nic nie zwraca) → **pomiń całą fazę** i przejdź do Fazy 3.

### 2.2 Runda — trzej audytorzy równolegle

Wywołaj przez Agent tool, wszystkich trzech **w jednej wiadomości**, żeby biegli równolegle:

| `subagent_type` | Zakres |
|---|---|
| `code-review:security-auditor` | sekrety, SAST, logika autoryzacji |
| `code-review:code-quality-auditor` | SOLID, granice kontekstów, konwencje |
| `code-review:documentation-auditor` | zgodność `docs/` ze zmianą |

**Nie wołaj komendy `/code-review:review`.** Zadaje pytania interaktywne i nie przyjmuje zawężenia zakresu.

Każdy prompt musi zawierać poniższe dwa bloki.

**Blok zakresu** — bez niego audytorzy skanują całe repo i runda trwa wielokrotnie dłużej:

> Oceniaj wyłącznie te pliki: `<lista z 2.1>`.
> Kontekst wolno czytać szerzej, ale każde znalezisko musi kotwiczyć się w pliku z listy.
> Pomiń `dependency-scanning`, gdy `.ai/config/pull-request.md` § „Checki w CI” wymienia skan zależności.
> Pomiń `linter-integration` — Faza 1 uruchomiła już lintery, typy i narzędzie granic modułów z bramki.

**Blok reguł projektu** — audytorzy pluginu są generyczni i nie znają konwencji projektu. Wklej do promptu treść [`.ai/config/code-review.md`](../../../.ai/config/code-review.md).

- Złamanie reguły z tego pliku jest znaleziskiem.
- Błąd spoza zakresu audytor tylko zgłasza. Issue zakłada orkiestrator według 2.6.
- Audytorzy zostają przy własnej skali znalezisk. Warunek wyjścia z 2.5 się nie zmienia.

### 2.3 Weryfikacja znalezisk

Po zebraniu wyników odpal `code-review:challenger` i `code-review:cross-verifier`, oba na komplecie znalezisk.

`challenger` odsiewa fałszywe alarmy i koryguje wagę. Bez niego pętla naprawia rzeczy, które nie są problemami.

### 2.4 Zastosuj fixy

**Zanim zastosujesz JAKIKOLWIEK fix, sprawdź go wobec 2.6.** Warunek stoi niżej w dokumencie, ale obowiązuje wcześniej niż ta sekcja.

Pętla stosuje fixy **bez pytania**. Po fixach uruchom Quality Gate z Fazy 1 ponownie.

Każdy test dopisany do fixa przepuść przez skill **`ba-mutation-check`** — cofnij naprawę, potwierdź czerwień, przywróć.

Czerwony gate naprawiasz według 1.1. Po 3 nieudanych próbach — STOP i raport.

### 2.5 Warunek wyjścia

Runda kończy pętlę, gdy nie zwróciła znaleziska powyżej **LOW**.

Twardy limit: **3 rundy**. Po trzeciej rundzie z otwartymi znaleziskami — STOP, raport stanu, **bez pusha**.

Każdy raport STOP z tej fazy podaje SHA i ścieżkę do snapshotu z 1.0. Bez tego użytkownik zostaje z własną pracą i autonomicznymi fixami wymieszanymi w jednym brudnym drzewie, bez granicy między nimi.

Znaleziska LOW trafiają do podsumowania dla użytkownika. Nie blokują pusha.

Runda druga i trzecia liczą diff od nowa. Fixy z poprzedniej rundy wchodzą do zakresu.

### 2.6 Decyzje w pętli

Pętla nie pyta użytkownika o kierunek poprawki. Rozstrzyga sama i zapisuje decyzję z powodem w opisie PR-a, w sekcji `## Co się zmienia`. Gdy PR już istnieje, dopisz decyzję przez `gh pr edit --body-file`.

| Sytuacja | Co robisz |
|---|---|
| Znalezisko `needs-decision` albo poprawka z więcej niż jednym rozsądnym kierunkiem | Wybierz opcję prostszą i zgodną ze źródłami z `pull-request.md` § „Obszary wrażliwe” |
| Poprawka dotyka ścieżki z `pull-request.md` § „Obszary wrażliwe” | Zastosuj, gdy naprawia zmianę z tej gałęzi |
| Poprawka wychodzi poza zakres gałęzi | Nie stosuj. Realny problem: załóż issue (skill `ba-github-issues create`). Hipotetyczny: pomiń |
| Poprawka wymagałaby wyjątku w konfiguracji narzędzia granic modułów | Przeprojektuj poprawkę, żeby wyjątek nie był potrzebny. Wyjątku nie dopisujesz nigdy |

**STOP** tylko wtedy, gdy żaden projekt poprawki nie mieści się w regułach narzędzia granic modułów albo poprawka wymaga destrukcyjnej operacji na bazie. Migracja, która kasuje dane (`DROP`, `TRUNCATE`, `DELETE`, zawężenie typu kolumny), też jest taką operacją.

### 2.7 Artefakty

Raporty audytorów zapisuje **orkiestrator** z tekstu zwróconego przez subagentów. Sami audytorzy tego nie zrobią — żaden z pięciu agentów używanych w tej fazie nie ma narzędzia `Write`.

Miejsce zapisu: `.claude/scratch/reviews/`. Katalog jest w `.gitignore`, więc raporty nie wejdą do commita niezależnie od tego, którą ścieżką skończy się pętla.

**Nie kieruj ich do `docs/reviews/`.** Ten katalog nie jest ignorowany, a Faza 2 ma wyjścia awaryjne (czerwony gate, wyczerpane rundy, STOP z 2.6), które nigdy nie docierają do sprzątania w Fazie 3.

## Faza 3 — Sprzątnięcie artefaktów review

Cel: usunąć efemeryczne pliki review, które nie powinny trafić do PR-a. Specyfikacje i plany superpowers przenieść do `.ai/specs/`.

```bash
for f in docs/superpowers/specs/*.md docs/superpowers/plans/*.md; do
  if test -f "$f"; then mv "$f" .ai/specs/ && echo "moved $f to .ai/specs/"; fi
done
test -d docs/reviews && rm -rf docs/reviews/ && echo "deleted docs/reviews/" || echo "no docs/reviews/ to delete"
test -d docs/superpowers && rm -rf docs/superpowers/ && echo "deleted docs/superpowers/" || echo "no docs/superpowers/ to delete"
```

**Specyfikacje i plany nie giną.** Superpowers zapisuje je domyślnie w `docs/superpowers/specs/` i `docs/superpowers/plans/`. Ich miejsce to `.ai/specs/` (`AGENTS.md` § Katalog `.ai/`). Przeniesiony plik zachowuje nazwę, a Faza 4 decyduje, czy idzie do `implemented/`.

**Co kasujemy:** `docs/reviews/` i to, co zostało w `docs/superpowers/` po przeniesieniu. Nic poza tym.

**Czego NIE tykamy:**
- `CLAUDE.md` (dokumentacja projektu, część repo).
- `.claude/` (settings, hooki, skille — wersjonowane, część repo).
- Innych plików zawierających „superpower" w nazwie poza wymienionymi katalogami — mogą być świadomie commitowaną dokumentacją projektu.

**Reguła:** jeśli użytkownik chce zachować coś innego z `docs/reviews/` lub `docs/superpowers/` — powinien commitować to zanim wywoła skill. Skill ratuje tylko specyfikacje i plany.

Ta faza idzie **za** pętlą review. Raporty z Fazy 2 żyją w `.claude/scratch/reviews/` i nie zależą od tego sprzątania — `docs/reviews/` kasujemy tu dlatego, że zapisuje tam komenda `/code-review:review`, gdy użytkownik odpali ją osobno.

## Faza 4 — Commit + push

1. **Wiedza do `.ai/`** (`AGENTS.md` § Katalog `.ai/`). Commit zabiera te pliki razem z kodem.
   - Poprawka dała regułę na przyszłość: lekcja w `.ai/lessons/` i wiersz w `.ai/lessons.md`.
   - Specyfikacja z `.ai/specs/` jest w całości zrobiona: `git mv` do `.ai/specs/implemented/`, razem z plikami o tym samym slugu i końcówce `-plan`, `-qa`, `-qa-report`.
   - Przebieg autonomiczny (`ba-auto-fix-issue`, `ba-fix-issue`, zadanie cezar): domknij dziennik przebiegu w `.ai/runs/`.

2. **Commit** (Conventional Commits + zasady CLAUDE.md):
   - Format: `<typ>(<scope>): <opis> (#<issue>)`
   - Typy: `feat`/`fix`/`refactor`/`docs`/`test`/`chore`/`perf`/`style`/`config`
   - **Bez sygnatur agenta** (NIE dodawaj `Co-Authored-By: Claude …` ani `🤖 Generated with …`) — globalna reguła z `~/.claude/CLAUDE.md`.

   ```bash
   git add -A
   git commit -m "<typ>(<scope>): <opis> (#<issue>)"
   ```

3. **Push** (gałąź bieżąca, nigdy gałąź główna):

   ```bash
   main_branch="<gałąź główna z pull-request.md>"
   current=$(git branch --show-current)
   case "$current" in "$main_branch"|main|master|develop) echo "ABORT: gałąź chroniona"; exit 1;; esac
   git push -u origin "$current"
   ```

## Faza 5 — Wystaw PR (tylko jeśli nie ma)

Sprawdź czy PR dla gałęzi już istnieje:

```bash
gh pr view --json number,url,state 2>/dev/null
```

- **Istnieje + state=OPEN** → przejdź do Fazy 6 (feedback).
- **Brak** → utwórz nowy, gotowy do review:

  ```bash
  gh pr create --base main --title "<typ>(<scope>): <opis> (#<issue>)" --body-file <plik z opisem>
  ```

  Opis i sposób wystawienia podaje `.ai/config/pull-request.md`:

  - `pull-request.md` § „Opis PR-a”: sekcje szablonu, draft albo gotowy PR, komenda lokalnego sprawdzenia opisu. Uruchom ją przed wystawieniem.
  - `pull-request.md` § „Dowód weryfikacji”: kiedy opis musi mieć dowód i jaki.

  Opis PR-a nie ma podpisu agenta. Bez stopki „Generated with Claude Code" i bez innej atrybucji.

- Jeśli issue z `Closes #N` w nazwie gałęzi (`feat/101-…` → issue 101) — dopisz `Closes #N` w sekcji `## Dlaczego`, by GitHub zamknął issue po merge.

- Decyzje podjęte według 2.6 wpisz do sekcji `## Co się zmienia`.

- Po utworzeniu wypisz URL PR-a wprost użytkownikowi.

- Potem Faza 6. Zaczyna się od czekania na sprawdzenia.

## Faza 5.5 — Resolve merge conflicts (jeśli PR DIRTY)

Cel: utrzymać PR mergeable. Konflikt z `main` (zwłaszcza po długo otwartym PR lub gdy main się przesunął) blokuje merge i sprawia że `mergeStateStatus = DIRTY`. Bez tej fazy czekanie z 6.6 trafiałoby na PR, którego nie da się scalić.

### 5.5.1 Detekcja

```bash
# pr_num: jeśli skill dostał numer PR-a jako argument (np. `/ba-ship-pr 214`),
# PODSTAW TEN NUMER wprost — pr_num="214". Inaczej oblicz z bieżącej gałęzi:
pr_num="$(gh pr view --json number -q .number)"
state=$(gh pr view "$pr_num" --json mergeStateStatus,mergeable -q '"\(.mergeStateStatus) \(.mergeable)"')
echo "PR #$pr_num: mergeStateStatus + mergeable = $state"
```

Wartości `mergeStateStatus` (GraphQL `PullRequestMergeStateStatus`):
- **CLEAN** — gotowy do merge (passuj do Fazy 6).
- **HAS_HOOKS** / **UNSTABLE** — mergeable, ale jakiś check failing (Faza 6 obsłuży feedback).
- **BLOCKED** — brakuje approval / required check (Faza 6 czeka na recenzję).
- **DIRTY** — REAL CONFLICT z main, wymaga rozwiązania.
- **UNKNOWN** — GH jeszcze nie skomputował; po `git push` minęły ≤ kilka sekund. Pollinguj raz, potem traktuj jak DIRTY/CLEAN po wyniku.

**Gałąź za `main` bez konfliktu zwykle nie wymaga działania.** Stan BEHIND GitHub zgłasza tylko wtedy, gdy ruleset gałęzi głównej wymaga gałęzi aktualnej z `main` (`strict_required_status_checks_policy: true`). Bez tej opcji gałąź w tyle ma zwykły stan (CLEAN, BLOCKED, UNSTABLE) i da się ją zmergować bez dociągania `main`.

Bieżącą wartość opcji sprawdzisz tak. Nazwę rulesetu bierzesz z `pull-request.md` § „Gałąź główna”. `gh api` sam podstawia `{owner}` i `{repo}` z katalogu roboczego.

```bash
ruleset="<nazwa rulesetu z pull-request.md>"
rs=$(gh api "repos/{owner}/{repo}/rulesets") || { echo "STOP: gh api rulesets nie działa"; exit 1; }
id=$(printf '%s' "$rs" | jq -r --arg n "$ruleset" '.[]|select(.name==$n).id')
test -n "$id" || { echo "STOP: brak rulesetu '$ruleset'"; exit 1; }
gh api "repos/{owner}/{repo}/rulesets/$id" \
  --jq '.rules[]|select(.type=="required_status_checks").parameters.strict_required_status_checks_policy'
```

Gdy zwraca `true` i PR ma BEHIND, idź ścieżką 5.5.2. Merge bez konfliktu sam tworzy commit, więc pomiń pkt 2–5. Przejdź od razu do pkt 6 (Quality Gate po merge) i pkt 7 (push).

**Pomiń tę fazę** gdy `mergeStateStatus` ≠ DIRTY (i ≠ BEHIND przy `strict_required_status_checks_policy: true`).

### 5.5.2 DIRTY (i BEHIND przy `strict`) — rozwiązywanie konfliktów

1. **Synchronizuj:**

   ```bash
   git fetch origin main
   git merge origin/main --no-edit || true   # nie wywalaj turn — chcemy zobaczyć pliki w konflikcie
   ```

2. **Zbierz pliki w konflikcie:**

   ```bash
   conflicted=$(git diff --name-only --diff-filter=U)
   echo "Konflikty w plikach:"
   echo "$conflicted"
   ```

3. **Klasyfikuj konflikt PER plik** zanim cokolwiek edytujesz:

   - **Plik blokady zależności** z `pull-request.md` § „Pliki blokad zależności” → regeneruj go komendą z tej tabeli zamiast resolve markerów.
     - Pliku blokady nigdy nie scalasz po znacznikach konfliktu. Zawsze generujesz go od nowa z manifestu.

   - **Plik shim / re-export / mechaniczny rename** → preferuj wersję z gałęzi feature (`git checkout --ours <plik>`) i ręcznie sprawdź czy odpowiada aktualnemu canonical path z main.

   - **Konfiguracja narzędzia granic modułów / config (toml/yaml/json)** → merge ręczny: czytaj OBA warianty, znajdź union sensu. Listy reguł i wyjątków często mają niezależne dodatki z każdej strony — łącz je.

   - **Plik źródłowy z prawdziwą logiką** → ręczny merge. Czytaj kontekst funkcji nie tylko hunków. Jeśli oba branche modyfikują tę samą linię z różnym celem → ESKALUJ do usera, nie zgaduj.

   - **Plik dokumentacji (`docs/**.md`, `CLAUDE.md`)** → ręczny merge. Częste konflikty na listach zmian w sekcji „Status" lub w tabelach. Łącz oba wpisy.

4. **Resolve per plik** (pętla):

   ```bash
   for f in $conflicted; do
     # Read pliku, znajdź markery <<<<<<<, =======, >>>>>>>
     # Edit usuwając markery + scalając treść świadomie
     git add "$f"
   done
   ```

   **Reguły:**
   - **NIGDY nie usuwaj kodu z konfliktu „bo szybciej" — to typowy regression vector.** Świadoma decyzja = pisemnie uzasadnij w głowie którego brancha treść zostaje i dlaczego.
   - Jeśli plik jest binarny (PDF, obrazek, lockfile) — preferuj regenerację z manifestu zamiast `--ours`/`--theirs` na ślepo.
   - Jeśli >5 plików w konflikcie LUB >50 linii w jednym pliku → STOP i poproś usera o kierunek (mała szansa na czystą maszynową resolve).

5. **Finalizuj merge:**

   ```bash
   git diff --name-only --diff-filter=U   # musi być puste
   git commit --no-edit   # akceptuj default merge message
   ```

6. **Quality Gate po merge** (CRITICAL — merge może obudzić konflikty semantyczne, których lint/test nie zobaczył w żadnej z gałęzi osobno):

   Uruchom pełną bramkę z 1.1, razem z podsekcjami warunkowymi. Czerwony krok naprawiasz według 1.1. Najczęstsza przyczyna: zmiana sygnatury w `main` i nowe wywołanie w gałęzi.

7. **Push:**

   ```bash
   git push
   ```

### 5.5.3 Gałąź cięta z gałęzi zmergowanej squashem

Jeśli gałąź wyszła nie z `main`, tylko z innej gałęzi feature, którą **zmergowano squashem**, to jej commity fizycznie nie są przodkami `main` — ich treść żyje w jednym squash-commicie. PR z bazą `main` pokaże wtedy dublety: commity poprzedniej gałęzi plus wszystkie własne.

Rozpoznanie:

```bash
git log --oneline origin/main..HEAD | wc -l        # podejrzanie dużo
gh pr list --head <poprzednia-gałąź> --state all --json number,state   # MERGED?
git merge-base --is-ancestor <tip-poprzedniej> origin/main && echo "w main" || echo "NIE w main (squash)"
```

**Zanim cokolwiek zrobisz, sprawdź czy gałąź jest już na `origin`:**

```bash
git ls-remote --heads origin "$(git branch --show-current)"
```

- **Niepusty wynik → STOP.** Gałąź jest wypchnięta. Naprawa wymagałaby przepisania historii i force-pusha, a to jest **zabronione** (`~/.claude/CLAUDE.md`). Opisz sytuację użytkownikowi i czekaj na decyzję. Nie proponuj `--force` ani `--force-with-lease` jako wyjścia.
- **Pusty wynik** → gałęzi nie ma na zdalnym, nie ma czego nadpisać. Możesz przenieść **tylko własne** commity na `origin/main`:

  ```bash
  git branch -f backup/<gałąź>-prerebase HEAD        # backup przed przepisaniem historii
  git rebase --onto origin/main <tip-poprzedniej-gałęzi> <twoja-gałąź>
  ```

  Po rebase **przepuść pełny Quality Gate** (jak w 5.5.2 pkt 6) — przeniesienie na nową bazę potrafi obudzić konflikt semantyczny, którego żadna gałąź nie widziała osobno. Dopiero potem zwykły `git push -u`.

### 5.5.4 ESKALACJA do usera

Eskaluj (STOP fazy 5.5) gdy:
- Konflikt w pliku z prawdziwą logiką biznesową (nie shim/lockfile/config) i recenzent nie jest dostępny do potwierdzenia.
- `git merge` raportuje konflikt w pliku NIE w `git diff --diff-filter=U` (rzadki edge case — symlink, tree conflict, rename/edit).
- Po resolve i merge Quality Gate czerwony, a fix wymaga zmian semantyki kodu z main.
- Konflikt w `.claude/` (settings/hooki) — to konfiguracja dev environment, nie kod, user powinien świadomie wybrać.

Format eskalacji: lista plików z konfliktem + jednolinijkowe podsumowanie typu konfliktu per plik + zapytanie „która strona zostaje?". NIE pushuj częściowo rozwiązanego stanu.

## Faza 6 — Krytyczny przegląd feedbacku z PR-a

To **najważniejsza** faza tego skilla. Default branch agenta to ślepe stosowanie sugestii — tutaj jest dokładnie odwrotnie: **nic nie wprowadzaj bez weryfikacji**.

**Limit: 3 rundy odpowiedzi na feedback**, licząc jak w 2.5. Runda to jeden cykl „przeczytaj uwagi → napraw → odpowiedz → push". Po trzeciej rundzie STOP: wypisz użytkownikowi, co zostało otwarte, i zostaw decyzję jemu.

Ten limit nie jest ostrożnością, tylko warunkiem zbieżności. Każda odpowiedź kończy się pushem, push odpala nowe review, a review zawsze coś znajdzie — im czystszy diff, tym drobniejsza uwaga. Bez limitu i bez progu z 6.3 PR nigdy nie osiąga stanu „skończony", bo proces sam produkuje sobie następne wejście.

Sygnał, że limit już zadziałał, a Ty go ignorujesz: recenzent pisze „gotowe do merge" i mimo to dorzuca uwagi. To znaczy, że zeszliście poniżej progu istotności — kończ.

### 6.0 Werdykt review AI czytaj z bloku

**Werdykt review AI czytasz z miejsca podanego w `pull-request.md` § „Werdykt review AI”.** Nie zgaduj go z treści recenzji. Ta sekcja podaje autora komentarza, kształt bloku werdyktu i komendę, która go pobiera.

- `verdict: approve` — check review zielony. Przy zielonych checkach PR merguje się według `pull-request.md` § „Merge”. Uwagi 🟡 weryfikuj według progu z 6.3. Poprawka po merge'u idzie nowym PR-em.
- `verdict: request_changes` — uwagi 🔴 trzymają check review na czerwono. Każdą i tak weryfikuj według 6.3.
- Uwaga 🔴, którą odrzucasz jako false positive, dostaje odpowiedź z uzasadnieniem. Odpowiedź plus push daje nową rundę, także gdy push niesie pusty commit (opcja `--allow-empty`).
- `<etykieta zablokowanego PR-a>` po 3 rundach: STOP, zgłoś użytkownikowi otwarte uwagi 🔴.

### 6.1 Pobierz feedback

**Najpierw skill `ba-wait-checks <pr_num>`.** Feedback czytasz dopiero po wyniku sprawdzeń. Dotyczy każdego wejścia do Fazy 6: po nowym PR-ze, po pushu do istniejącego PR-a i po ponownym wywołaniu bez pushu. Raport zachowaj dla 6.6.

`gh pr view --json` zwraca tylko top-level `comments` (issue comments) i `reviews` (review summaries). Inline **review comments** (zaczepione na konkretny plik:linia) NIE są wystawione przez `gh pr view` w obecnej wersji `gh` — pobierane są osobno przez REST API GitHuba.

```bash
# pr_num: jeśli skill dostał numer PR-a jako argument (ponowne wywołanie: `/ba-ship-pr <n>`),
# PODSTAW TEN NUMER wprost — pr_num="<n>". Inaczej oblicz z bieżącej gałęzi:
pr_num="$(gh pr view --json number -q .number)"
repo=$(gh repo view --json nameWithOwner -q .nameWithOwner)

# (a) Issue comments (top-level dyskusja na PR) + review summaries
gh pr view "$pr_num" --json comments,reviews,state,statusCheckRollup

# (b) Inline review comments (najcenniejsze — mają konkretne plik:linia)
gh api "repos/$repo/pulls/$pr_num/comments" --paginate
```

Jeśli skill został wywołany z numerem PR-a jako argumentem — użyj go. W przeciwnym razie PR bieżącej gałęzi.

Pola w outpucie REST API `pulls/{n}/comments`:
- `path`, `line` (lub `original_line` dla starych komentarzy) — lokalizacja
- `body` — treść uwagi
- `user.login`, `id`, `in_reply_to_id` (gdy reply na thread)
- `position` (NULL gdy outdated, dotyczy nieistniejącego już diffa)

Łącz oba źródła w jedną listę uwag do weryfikacji.

### 6.2 Filtrowanie szumu

Pomiń (ale wypisz że pomijasz, żeby było widać):
- Komentarze z `position: null` w inline review comments — dotyczą outdated diff (kod się zmienił, kotwica „odpadła"). Sprawdź `original_line` ale traktuj jako historyczne, zwykle nieaktualne.
- Komentarze emoji-only / „LGTM" / akceptacje (`reviews[].state == "APPROVED"` bez `body`)
- Komentarze bota CI z linkiem do logu (potraktuj jako pointer do CI, nie jako finding)
- Self-comments (autor PR-a = autor komentarza) — często to TODO-notki autora, nie feedback

### 6.3 Krytyczna weryfikacja każdej uwagi

Dla **KAŻDEJ** zostającej uwagi WYKONAJ w tej kolejności:

1. **Wczytaj plik na wskazanej linii** (`Read` z `offset/limit`). Nie ufaj cytatowi z komentarza — przeczytaj aktualny kod.
2. **Sprawdź czy problem realnie istnieje:**
   - Czy kod istotnie ma opisaną wadę?
   - Czy claim recenzenta opiera się na rozumieniu kodu, czy na założeniach o kontekście? (np. „to leak" — czy faktycznie zasób nie jest zamykany? czy może jest, kontekst-manager wyżej?)
   - Czy recenzent zna projektowe konwencje (AGENTS.md, ADR-y)? Jeśli to opinia stylowa sprzeczna z naszą konwencją — odrzuć.
   - Czy fix poprawiłby coś mierzalnego (bug, perf, security, czytelność) czy tylko przesunąłby preferencję?
3. **Odsiej po istotności, ZANIM zaczniesz klasyfikować.** Próg jest ten sam co w 2.5: reaguj na znaleziska **powyżej LOW**. Uwaga oznaczona `[Low]`, `[nit]`, „drobiazg", „do rozważenia" albo taka, którą sam recenzent opatrzył zdaniem „nie blokuje merge" — **nie jest fixowana**. Trafia do podsumowania dla użytkownika i do odpowiedzi w PR jako świadomie pominięta.

   Bez tego progu Faza 6 nie ma końca. Każda odpowiedź to push, każdy push to nowe review, a review zawsze znajdzie kolejny nit — im czystszy diff, tym drobniejsze uwagi. Faza 2 ma warunek wyjścia; ta musi mieć taki sam, inaczej PR szlifuje się w nieskończoność.

   Wyjątek: uwaga formalnie LOW, ale opisująca **utratę danych, lukę bezpieczeństwa albo nieprawdę w dokumentacji** — te traktuj jak MEDIUM niezależnie od etykiety recenzenta.

4. **Klasyfikuj uwagę jako jedną z:**
   - **Valid + apply** — realny problem, fix ma sens, niska ryzyko regresji → zastosuj
   - **Valid + defer** — realny problem, ale zakres niewystarczający na tym PR → otwórz issue follow-up zamiast fixować inline
   - **False positive** — claim niezgodny z rzeczywistością (np. kod już to robi, edge case zaadresowany gdzie indziej, recenzent nie widział pełnego kontekstu)
   - **Style/preference** — sprzeczne z konwencją projektu lub zwykła preferencja recenzenta bez technicznej podstawy → odrzuć
   - **Niejasne** — zapytaj recenzenta o doprecyzowanie, nie wprowadzaj zgadywanego fixa

5. **NIE ufaj autorytetowi recenzenta.** Senior + „to jest źle" ≠ realny problem. Argument > stopień.

6. Dla każdej uwagi zaraportuj klasyfikację z **jednym zdaniem uzasadnienia opartego o sprawdzony kod**, NIE o cytat z komentarza. Uwagi odsiane w punkcie 3 wypisz zbiorczo, jednym zdaniem — żeby było widać, co pominięto świadomie.

### 6.4 Zastosuj fixy (tylko `valid + apply`)

- **Tabela z 2.6 obowiązuje też tutaj.** Feedback z PR-a to wejście zewnętrzne: komentarz recenzenta albo bota może popchnąć edycję obszaru wrażliwego. Poprawki, która wychodzi poza zakres gałęzi, nie stosuj. Uwagę dotykającą obszaru z `pull-request.md` § „Obszary wrażliwe” zastosuj dopiero wtedy, gdy potwierdzisz błąd niezależną drogą: testem, zapytaniem na lokalnej bazie albo prześledzeniem kodu.
- Wprowadź zmiany.
- **Każdy test dopisany do fixa zweryfikuj mutacyjnie** — skill **`ba-mutation-check`**. Cofnij naprawę, potwierdź, że test pada, przywróć. Test regresyjny, którego nie widziałeś na czerwono, bywa zielony z zupełnie innego powodu niż naprawa; taki test przechodzi review i nie chroni przed niczym.
- Uruchom Quality Gate ponownie (Faza 1) — fixy mogą złamać coś innego.
- Commit:

  ```bash
  git add -A
  git commit -m "fix(<scope>): address PR feedback (<krótki opis>)"
  ```

  Jeśli wszystkie fixy są trywialne i logicznie jeden temat — jeden commit. Inaczej rozdziel logicznie (każdy commit niezależnie zielony).

- Push: `git push`.
- Po odpowiedziach z 6.5: powrót do 6.1. Zaczyna się od czekania na sprawdzenia nowego commita.

### 6.5 Odpowiedź na feedback

Dla każdej uwagi odpowiedz w PR przez `gh pr comment "$pr_num" --body "..."` lub przez reply na thread (jeśli `gh` wspiera w danej wersji).

Format odpowiedzi per uwaga:

- **Valid + applied:** „Naprawione w `<short-sha>` — <jedno zdanie co się zmieniło>."
- **Valid + deferred:** „Słuszne, ale poza zakresem tego PR — założyłem follow-up issue #N."
- **False positive:** „Sprawdziłem — kod robi już X w <plik:linia>, więc tutaj nie ma problemu. Daj znać jeśli widzisz inny scenariusz."
- **Style/preference:** „Projekt świadomie stosuje konwencję X (patrz <AGENTS.md / docs/>), więc zostawiam jak jest."
- **Niejasne:** „Mógłbyś doprecyzować — masz na myśli <interpretacja A> czy <B>?"

Odpowiadaj zwięźle i rzeczowo. Bez „you might want to consider" i bez kapitulanckich „good point" jeśli faktycznie nie ma punktu.

### 6.6 Wynik sprawdzeń

Raport `ba-wait-checks` wybiera dalszy krok. Przed tabelą sprawdź `mergeStateStatus`: `gh pr view "$pr_num" --json state,mergeStateStatus`.

| Stan | Krok |
|---|---|
| PR `MERGED` albo `CLOSED` | Koniec. |
| `mergeStateStatus` = DIRTY (albo BEHIND przy `strict_required_status_checks_policy: true`, patrz 5.5.1) | Faza 5.5, potem 6.1. Nie czekaj na recenzenta na PR-ze, którego nie da się zmergować. |
| Zielone, bez nowych uwag powyżej progu z 6.3 | Koniec. Uwagi poniżej progu wypisz użytkownikowi jako pominięte. |
| Czerwone tylko przez prośbę człowieka o zmiany, każda jego uwaga ma odpowiedź z 6.5 | Koniec. Raport: PR czeka na ponowne review od tej osoby. GitHub trzyma prośbę do jej kolejnego review. |
| Czerwone albo nowe uwagi powyżej progu | Powrót do 6.1, w limicie 3 rund. Czerwony check naprawiasz według 6.6a. |
| Trwa po limicie czekania `ba-wait-checks` | Raport stanu każdego sprawdzenia i koniec tury. Kolejne `/ba-ship-pr <pr_num>` podejmie pracę. |
| PR ma `<etykieta zablokowanego PR-a>` albo wyczerpane 3 rundy | Koniec, raport otwartych uwag do użytkownika. |

Werdykt `approve` w bloku z 6.0 i zielone checki to PR gotowy do merge'a. Pieczątka (`reviewDecision`) się nie liczy, gdy różni się od bloku.

#### 6.6a Czerwony CI: naprawa

`ba-wait-checks` podaje przy każdym czerwonym checku werdykt: wina gałęzi albo gałąź główna też by dziś padła. Drugi werdykt nie zwalnia z naprawy.

Naprawa idzie jak w 6.4: Quality Gate, commit, push. Potem powrót do 6.1. Naprawa czerwonego checku liczy się jako runda z limitu 3.

Przy werdykcie „gałąź główna też by padła” w opisie PR-a i w odpowiedzi recenzentowi napisz wprost, że defekt jest niezależny od zmian — inaczej ktoś będzie szukał winy w twoim diffie.

Dla podatności w pliku blokady zależności: podbij **tylko** dotknięty pakiet komendą z `pull-request.md` § „Pliki blokad zależności”, nie cały plik.

Diff pokaże wtedy jedną zmianę **wersji** — ale niekoniecznie jeden pakiet. Ponowne wygenerowanie pliku potrafi przy okazji zmienić inne wpisy. To nie jest przypadkowa regeneracja całego pliku. Sprawdź diff według `pull-request.md` § „Pliki blokad zależności”, zanim uznasz za błąd. **Opisz wynik w PR** zamiast twierdzić „jedna zależność" — recenzent zweryfikuje diff i znajdzie rozbieżność.

## Stop conditions

- **STOP** jeśli nie ma zmian, commitów ponad `main` ani PR-a — nic do wysłania.
- **STOP** jeśli jesteś na gałęzi głównej z `pull-request.md` — nigdy nie commituj/push z main przez ten skill.
- **STOP** jeśli Quality Gate jest czerwony po 3 próbach naprawy (1.1) — nie wypychaj, zgłoś użytkownikowi.
- **STOP** jeśli pre-commit hook blokuje commit — eskaluj, nie hackuj wokół.
- **STOP** jeśli `gh auth status` nie wskazuje aktywnej sesji — poproś użytkownika o `gh auth login`.
- **STOP** jeśli pętla review z Fazy 2 wyczerpała 3 rundy z otwartymi znaleziskami — nie pushuj, zgłoś stan.
- **STOP** przy awarii infrastruktury: brak sieci, bazy, zmiennych środowiskowych.
- **STOP** z 2.6: brak projektu poprawki zgodnego z regułami narzędzia granic modułów albo destrukcyjna operacja na bazie.
- **STOP** przy konflikcie scalania z 5.5.2-5.5.4, który wymaga decyzji użytkownika.
- **STOP** jeśli recenzent dał `CHANGES_REQUESTED` bez komentarzy w kodzie albo sprawdzenia trwają po limicie czekania `ba-wait-checks` (6.6).
- **STOP** jeśli Faza 6 wyczerpała 3 rundy odpowiedzi na feedback albo jedyne nowe uwagi są poniżej progu z 6.3 — wypisz pominięte, oddaj decyzję użytkownikowi.

## Co robi, czego nie robi

**Robi:**
- Uruchamia Quality Gate.
- Przepuszcza diff przez lokalną pętlę review (audytorzy pluginu `code-review` zawężeni do zmienionych plików, maks. 3 rundy) i sam stosuje fixy.
- Przenosi specyfikacje i plany z `docs/superpowers/` do `.ai/specs/`, potem kasuje `docs/reviews/` i `docs/superpowers/` (artefakty working-review).
- Commituje, pushuje, wystawia PR.
- Wykrywa konflikty merge z main (`mergeStateStatus` = DIRTY) i je rozwiązuje (lockfile regen / shim preferencja / ręczny merge per plik / Quality Gate po merge). Eskaluje do usera gdy konflikt wymaga decyzji biznesowej.
- Pobiera feedback z PR-a i krytycznie go weryfikuje.
- Stosuje TYLKO te fixy które przeszły weryfikację „realny problem".
- Odpowiada w PR per uwaga.
- Po każdym pushu czeka na wynik każdego sprawdzenia przez skill `ba-wait-checks` i raportuje stan z GitHuba, nigdy przewidywanie.

**Nie robi:**
- Nie mergeuje PR-a sam. Merge robi auto-merge GitHuba.
- Nie zamyka issue ręcznie — GitHub zamknie sam po merge przez `Closes #N`.
- Nie sygnuje commitów jako agent.
- Nie stosuje sugestii recenzenta bez sprawdzenia kodu.
- Nie czyści `docs/reviews/` ani `docs/superpowers/` PRZED Quality Gate'em i pętlą review — żeby user widział, co byłoby skasowane, gdyby gate się wyłożył.
- Nie zastępuje review na GitHubie. Faza 2 ma zmniejszyć liczbę rund, nie usunąć zdalne sprawdzenie — tamto startuje na czystym kontekście i łapie to, czego pętla w tej samej sesji nie zobaczy.
