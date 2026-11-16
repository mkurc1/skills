---
name: ba-wait-checks
description: "Use right after pushing a branch that has an open GitHub pull request, before reporting its state — waits for every check on the latest commit and for any human review the pull request is waiting on, then reports each result as GitHub gives it, never a prediction. Judges every red check (branch fault or would the main branch fail too). Called by ba-ship-pr after each push; also runnable alone as /ba-wait-checks [<pr>]. Read-only: never fixes, pushes or replies."
---

# /ba-wait-checks — wynik każdego sprawdzenia PR-a

Wejście: numer PR-a. Wynik: raport ze stanem każdego sprawdzenia, wzięty z GitHuba.

**Stan sprawdzenia podajesz tylko z wyjścia skryptu `scripts/wait.sh`.** Nie kończysz tury z przewidywaniem w stylu „powinno być zielone”. Coś jeszcze trwa? Piszesz „trwa”.

## Pojęcia

| Pojęcie | Znaczenie |
|---|---|
| Sprawdzenie | Check na ostatnim commicie PR-a albo review od człowieka, na które PR czeka. |
| Check | Wynik zadania CI albo aplikacji na commicie. Recenzent AI w CI to też check albo review na GitHubie. |
| PR czeka na człowieka | PR ma prośbę o review albo GitHub wymaga zatwierdzenia przed merge'em. |

Skill działa w każdym repo na GitHubie: z pełnym CI, z samym recenzentem, z obydwoma albo bez niczego.

## Wywołanie

| Wywołanie | Co robi | Co zostawia |
|---|---|---|
| `/ba-wait-checks [<pr>]` | Czeka na wynik każdego sprawdzenia PR-a, najwyżej 60 min. Ocenia każde czerwone. | Raport stanu. Repo i PR bez zmian. |

Bez numeru skill bierze PR bieżącej gałęzi: `gh pr view --json number -q .number`.

## Konfiguracja

Na początku pracy przeczytaj ten plik z `.ai/config/`:

| Plik | Co daje |
|---|---|
| `pull-request.md` | gałąź główna, główny workflow CI do porównania z gałęzią główną |

**Brak pliku** zatrzymuje skill. Podaj użytkownikowi nazwę brakującego pliku. Brakujące pliki generuje skill `ba-setup`.

Przykłady poleceń piszą gałąź główną jako `main`. Inną nazwę podstawiasz.

## Kroki

1. **Czekanie.** Uruchom skrypt z katalogu tego skilla:

   ```bash
   <katalog skilla>/scripts/wait.sh <pr> 540 <sha>
   ```

   - `<sha>` to `git rev-parse HEAD`, gdy bieżąca gałąź jest gałęzią PR-a. Skrypt czeka, aż GitHub przestawi PR na ten commit. Inaczej widziałby checki starszego commita.
   - Bieżąca gałąź to inna gałąź? Pomiń `540 <sha>`.
   - Jedno wywołanie trwa najwyżej 9 min. Skrypt odpytuje GitHuba co 30 s i kończy się zaraz po wyniku.
   - **Limit czasu polecenia powłoki ustaw na 10 min.** Domyślny limit narzędzia bywa krótszy i ubija skrypt bez kodu wyjścia.
   - Narzędzie ma polecenia w tle? Możesz uruchomić skrypt w tle i poczekać na jego koniec.
   - Kod wyjścia wybiera następny krok.

   | Kod | Znaczenie | Następny krok |
   |---|---|---|
   | 0 | Wszystko skończone i zielone, nie ma na co czekać albo PR jest zmergowany lub zamknięty (linia `result: merged` albo `result: closed`) | Raport |
   | 1 | Coś czerwone: check padł albo został anulowany, człowiek prosi o zmiany albo PR ma konflikt scalania | Ocena czerwonego, potem raport |
   | 2 | Coś jeszcze trwa | Uruchom skrypt ponownie |
   | 3 | Awaria: brak sesji `gh`, brak sieci, PR nie istnieje | Zatrzymanie |

2. **Limit.** Kod 2 dostaje kolejne wywołanie, łącznie najwyżej 60 min czekania. Po limicie raport podaje, co trwa.
3. **Ocena czerwonego checku.** Zanim przypiszesz winę gałęzi, odpowiedz: czy gałąź główna też by dziś padła?

   ```bash
   gh run view <run_id> --json jobs -q '.jobs[] | select(.conclusion=="failure") | .steps[] | select(.conclusion=="failure") | .name'
   git diff --stat origin/main..HEAD -- <plik, którego dotyczy błąd>
   gh run list --branch main --workflow <workflow CI> --limit 3 --json conclusion,createdAt
   ```

   - `<run_id>` stoi w linku checku z raportu skryptu.
   - Link checku nie prowadzi do GitHub Actions? Check pochodzi z zewnętrznej aplikacji. Otwórz link, opisz błąd i daj werdykt „nieustalone”.
   - `<workflow CI>` to główny workflow z `pull-request.md` § „Checki w CI”.
   - Werdykt „gałąź główna też by padła”: gałąź nie tykała pliku, a gałąź główna była zielona przed pojawieniem się przyczyny. Przykład: świeża podatność w zależności, wygasły token, awaria zewnętrznej usługi.
   - W przeciwnym razie werdykt „wina gałęzi”.
   - Prośba człowieka o zmiany nie dostaje oceny. Raport podaje ją wprost.
   - Konflikt scalania też nie. GitHub nie uruchamia wtedy checków, więc raport podaje konflikt zamiast listy checków.
4. **Awaria.** Kod 3 zatrzymuje skill. Raport podaje błąd ze skryptu.

## Raport

```
**Sprawdzenia PR #<n>** — zielone / czerwone / trwa po 60 min / brak sprawdzeń / PR zmergowany / PR zamknięty
- <check>: <wynik> — <link>
- Review od człowieka: <stan albo „PR nie czeka na człowieka”>
- Czerwone: <check> — wina gałęzi / gałąź główna też by padła / nieustalone, z jednym zdaniem dowodu
```

- Wyniki przepisujesz ze skryptu. Nie dopisujesz checków, których skrypt nie pokazał.
- Repo bez checków i bez recenzenta: piszesz to wprost. Skrypt czeka wtedy 2 min na pojawienie się checków, potem raportuje brak.

## Co robi, czego nie robi

**Robi:**
- Czeka na wynik każdego sprawdzenia PR-a.
- Ocenia każdy czerwony check.
- Raportuje stan wzięty z GitHuba.

**Nie robi:**
- Nie naprawia kodu, nie commituje i nie pushuje.
- Nie odpowiada na uwagi w PR-ze.
- Nie przewiduje wyniku sprawdzenia, które trwa.
