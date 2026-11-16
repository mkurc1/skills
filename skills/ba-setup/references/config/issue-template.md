# Szablon issue

Ten plik podaje szablon treści issue i zasady jego wypełniania. Czyta go skill `ba-github-issues`, który kopiuje blok poniżej.

## Szablon

```markdown
## Dlaczego
{1–3 zdania: problem, potrzeba albo obserwacja. Bug: objaw i skąd wiadomo.}

## Gotowe, gdy
- {Obserwowalny wynik, który da się sprawdzić.}

## Dowód
{Plik i linia, zapytanie albo log. Wymagany dla bug i follow-upu.}

## Zakres
- W zakresie: {…}
- Poza zakresem: {…}
- Decyzje do podjęcia w specyfikacji: {wybory techniczne, które rozstrzygnie plan; pomiń, gdy brak}

## Zależności
- {blokuje #X / zależy od #Y / wymaga ADR}
```

## Reguły

- Wymagane są sekcje „Dlaczego” i „Gotowe, gdy”.
- Pozostałe sekcje są opcjonalne. Pustą sekcję pomijasz w całości.
- Placeholdery dają tylko krótką podpowiedź. Reguły gotowości stoją w [`definition-of-ready.md`](definition-of-ready.md).
- Zakładaj issue przez `gh issue create --body-file <plik>`.
- Treść wielosekcyjna w `--body` łamie cudzysłowy.
