---
name: ba-mutation-check
description: Use immediately after writing or changing a test that is meant to catch a specific bug — regression tests, tests added during code review, tests for a fix you just made. Verifies the test actually fails when the fix is reverted, instead of passing for an unrelated reason. A green test proves nothing until you have seen it go red. Works in any language; the single-test command comes from .ai/config/project.md.
---

# ba-mutation-check — dowód, że test cokolwiek łapie

**Zielony test nie jest dowodem.** Test napisany do konkretnego błędu jest wart tyle, ile jego zdolność do upadku, gdy ten błąd wróci. Dopóki nie widzisz, jak pada, wiesz tylko, że przechodzi. Przechodzi też test, który nie sprawdza niczego.

Procedura zajmuje kilkadziesiąt sekund. Wyłapuje testy fałszywie zielone, których recenzent nie odróżni od dobrych.

## Wywołanie

| Wywołanie | Co robi | Co zostawia |
|---|---|---|
| `/ba-mutation-check` | Cofa naprawę, sprawdza, że test pada, przywraca naprawę. | Kod jak przed sprawdzeniem i wynik do raportu. |

## Konfiguracja

Na początku pracy przeczytaj ten plik z `.ai/config/`:

| Plik | Co daje |
|---|---|
| `project.md` | sekcja „Pojedynczy test”: polecenie, które uruchamia jeden plik testów |

**Brak pliku albo sekcji** zatrzymuje skill. Podaj użytkownikowi nazwę brakującego pliku. Brakujące pliki generuje skill `ba-setup`.

Sekcja ma kilka podsekcji stosów? Bierzesz polecenie stosu, do którego należy plik testu.

Polecenie z „Pojedynczy test” w `project.md` omija pamięć podręczną narzędzia testów. Bez tego mutacja może biec na starym kodzie. Przykłady takich pułapek: [`references/tool-pitfalls.md`](references/tool-pitfalls.md).

## Kiedy odpalać

**Zawsze** po napisaniu testu, który ma chronić przed konkretnym błędem:

- test regresyjny do poprawki błędu;
- test dopisany na żądanie recenzenta;
- test do świeżo naprawionej ścieżki obronnej: strażnika, walidacji, rozstrzygania remisu;
- test na niezmiennik, czyli warunek, który nigdy nie może zostać złamany.

**Nie trzeba** przy testach opisowych: szczęśliwa ścieżka nowej funkcji, test dymny. Tam nie ma jednego błędu, przed którym test broni.

## Procedura

```
1. Test przechodzi na naprawionym kodzie.   → polecenie z „Pojedynczy test”
2. Cofnij naprawę w kodzie produkcyjnym.    → mutacja
3. Test MUSI paść.                          → przechodzi? test jest bezwartościowy
4. Przywróć naprawę.                        → z kopii albo z commita
5. Test znów przechodzi.                    → nic nie zostało po mutacji
```

Tylko krok 3 cokolwiek dowodzi. Kroki 1 i 5 pilnują, żebyś nie zostawił śmieci.

Mutuj **kod produkcyjny**, nigdy test. Mutacja to dokładne cofnięcie naprawy: jedna linia, jeden warunek, jeden argument. Nie „coś zepsuj”.

## Cofanie mutacji

**Mutację cofasz z kopii pliku albo z zacommitowanego stanu.** Nigdy z pamięci.

- **Nigdy `git checkout` na niezacommitowanej poprawce.** `git checkout -- <plik>` przywraca plik do `HEAD`, czyli sprzed poprawki. Kolejna mutacja biegnie wtedy na kodzie bez naprawy, a test pada z innego powodu.
- Poprawka nie jest zacommitowana? Zrób kopię pliku przed mutacją.
- Po każdym cofnięciu sprawdź `git status` i `git diff`. Plik ma wrócić do stanu sprzed mutacji, nie do `HEAD` sprzed pracy.
- Piszesz plan z krokiem mutacji? Krok cofa mutację z kopii, gdy poprawka czeka jeszcze na commit.

```bash
orig=$(mktemp)
cp "<plik produkcyjny>" "$orig"
# ... mutacja i polecenie z „Pojedynczy test” ...
cp "$orig" "<plik produkcyjny>"
```

Kopia idzie do pliku z `mktemp`. Stała ścieżka, na przykład `/tmp/orig`, zderza się z kopią z innej sesji.

## Mutacja skryptem

Gdy mutacja ma jedną linię, podmień ją skryptem. Skrypt edytuje tylko tekst, więc działa dla pliku w każdym języku. Wymaga `python3` w systemie. Bez niego podmień linię edytorem i sprawdź `git diff`, że zmieniła się dokładnie ta jedna linia. Cały blok idzie jednym wywołaniem powłoki. Nieudany assert przerywa blok, zanim test pobiegnie na niezmutowanym kodzie.

Kotwica to fragment kodu, który skrypt wyszukuje i podmienia.

```bash
orig=$(mktemp)
cp "<plik>" "$orig"
python3 - <<'PY' || exit 1
import pathlib
p = pathlib.Path("<plik>"); s = p.read_text()
anchor = "<naprawiona linia>"
assert s.count(anchor) == 1, f"ambiguous anchor ({s.count(anchor)} hits), pick a longer fragment"
mutated = s.replace(anchor, "<linia sprzed naprawy>", 1)
assert mutated != s, "mutation not applied, check the anchor"
p.write_text(mutated)
PY
<polecenie z „Pojedynczy test”> "<plik testu>"   # MUSI paść
cp "$orig" "<plik>"
<polecenie z „Pojedynczy test”> "<plik testu>"   # MUSI przejść
git status --short "<plik>"
```

Oba asserty łapią **różne** awarie:

- `count(anchor) == 1`. Niejednoznaczna kotwica zmutowałaby też niepowiązane miejsca. Test padłby z innego powodu, a wynik wyglądałby na sukces. Z tego samego powodu `replace` ma limit `1`.
- `mutated != s`. Literówka w kotwicy daje cichą nieudaną podmianę i zielony test o niczym.

## Gdy test przechodzi mimo mutacji

Test **nie testuje tego, co myślisz**. Ustal dlaczego, zanim napiszesz go od nowa.

- **Dane testowe nie wyzwalają ścieżki.** Ranking w grupie z jednym elementem daje zawsze pierwsze miejsce. Wynik zgadza się przypadkiem, nie dzięki naprawie. Lek: dołóż drugi element.
- **Biblioteka przypadkiem oddaje właściwy wynik.** Zapytanie `ORDER BY created_at DESC LIMIT 1` bez drugiego klucza jest niedeterministyczne. Baza testowa akurat zwraca oczekiwany wiersz. Lek: sprawdzaj prawdziwy niezmiennik, tu treść wysłanego zapytania, nie wynik.
- **Asercja jest za słaba.** Asercja to warunek, który test sprawdza. `result is not None` przechodzi prawie zawsze. Lek: sprawdzaj wartość, nie istnienie.
- **Test buduje wejście ręcznie.** Produkcja składa je inaczej, więc obie strony są zielone i niezgodne. Lek: zbuduj wejście tą samą funkcją co produkcja.

## Przykłady mutacji

| Naprawa | Mutacja |
|---|---|
| `if "." in text: text = text.rstrip("0")` | usuń warunek `if` |
| obsługa wyjątku węższego przed szerszym | zamień kolejność obsługi |
| sortowanie po dwóch kluczach | usuń drugi klucz |
| `if not isinstance(result, dict): return {}` | usuń strażnika |
| funkcja odrzuca wartości `<= 0` | zwróć wartość bez filtra |

## Raportowanie

Opisujesz naprawę w PR-ze, w lekcji albo w odpowiedzi recenzentowi? Napisz **wprost**, że test przeszedł weryfikację mutacyjną i co mutowałeś. „Dodałem test” znaczy mniej niż „usunięcie strażnika wywala nowy test”.

Mutacja pokazała, że pierwsza wersja testu była fałszywie zielona? Napisz to. To najcenniejsza informacja w zgłoszeniu.

## Czego ten skill nie robi

To nie jest uruchomienie narzędzia do testów mutacyjnych na całym repozytorium, na przykład `mutmut` albo Stryker. To ręczne sprawdzenie **jednego** testu przeciw **jednej** naprawie. Trwa krócej niż napisanie testu.
