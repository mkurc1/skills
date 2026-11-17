# Szablon specyfikacji

Kiedy powstaje specyfikacja: każde issue przed kodem, według [`.ai/docs/sdlc.md` § Cykl życia zadania](../docs/sdlc.md#cykl-życia-zadania).

Plik leży w `.ai/specs/YYYY-MM-DD-slug.md`. Repo nie ma słownika pojęć. Termin definiujesz jednym zdaniem w specyfikacji.

## Wersja pełna

```markdown
# Tytuł zmiany

Issue: #N

## Cel
Problem i stan po zmianie, 1-3 zdania.

## Zakres
- Co wchodzi.

### Poza zakresem
- Czego nie robimy i dlaczego.

## Projekt
Gdzie mieszka reguła, przepływ danych, zmiany w modelach i API.

## Plan
1. Krok — jak go sprawdzić.

## Gotowe gdy
- Kryterium do sprawdzenia testem albo komendą.

## Ryzyka i otwarte pytania
- …
```

## Wersja krótka dla błędu

```markdown
# Tytuł błędu

Issue: #N

## Objaw
Co widać i jak to odtworzyć.

## Przyczyna
Gdzie w kodzie i dlaczego.

## Poprawka
Co się zmienia i gdzie mieszka reguła.

## Test regresyjny
Test, który pada przed poprawką.

## Gotowe gdy
- Kryterium do sprawdzenia testem albo komendą.
```
