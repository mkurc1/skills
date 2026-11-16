# Zasady pracy z issue

Ten plik uzupełnia `SKILL.md`. Opisuje reguły gita i częste błędy. Reguły operacji stoją w `SKILL.md`. Nazwy etykiet są logiczne. Prawdziwe nazwy stoją w `.ai/config/statuses.md` i `.ai/config/labels.md`.

## Reguły gita

- Polecenia `gh issue edit`, `comment`, `create`, `close` nie są operacjami gita. Wykonuj je swobodnie w ramach zadania.
- `gh label create` uruchamia użytkownik. Skill tylko pokazuje polecenie.
- Gałąź, commit, push i PR podlegają regułom gita z sesji. Ten skill ich nie nadpisuje.
- `gh issue develop` tworzy gałąź. Traktuj go jak tworzenie gałęzi.
- Nie podpisuj commitów ani PR-ów jako agent.

## Częste błędy

| Błąd | Naprawa |
| --- | --- |
| Komentarz „rozpocząłem pracę” przy starcie | Zob. `start`. |
| Issue bez etykiet wymaganych przez `labels.md` | Nadaj je według reguł z `labels.md`. |
| Dwie etykiety stanu naraz | Zob. `start` i `close`. |
| Ręczne `gh issue close` mimo PR-a z `Closes #<n>` | Zob. `close`. |
| Nazwa gałęzi niezgodna z `project.md` | Zbuduj ją według sekcji „Gałąź”. |
| Treść wielosekcyjna w `--body` | Użyj `--body-file`. |
| Agent sam zakłada brakującą etykietę | Pokaż polecenie `gh label create`. Etykietę zakłada użytkownik. |
| Komentowanie każdego kroku | Zob. `comment`. |
