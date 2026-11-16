# Szablon planu

Plan opisuje wykonanie specyfikacji krok po kroku. Leży w `.ai/specs/YYYY-MM-DD-slug-plan.md`, obok specyfikacji. Slug specyfikacji nie kończy się na `-plan`.

````markdown
# {Tytuł} — plan implementacji

Issue: #{n}

**Cel:** {Co działa po zmianie, 1-2 zdania.}

**Architektura:** {2-3 zdania: gdzie mieszka zmiana, kolejność prac.}

Specyfikacja: [`.ai/specs/{YYYY-MM-DD-slug}.md`]({YYYY-MM-DD-slug}.md)

## Ograniczenia globalne

- {Wartość wiążąca wszystkie zadania: nazwa, format, zakaz.}

## Na co uważać

- **{Ryzyko}.** {Wejście albo warunek, którego testy nie pokrywają, i które zadanie to sprawdza.}

---

### Task {k}: {nazwa}

**Pliki:**
- Utwórz: `{ścieżka}`
- Zmień: `{ścieżka}:{wiersze}`

**Interfejsy:**
- Wymaga: {co daje wcześniejsze zadanie}
- Dostarcza: {co biorą późniejsze zadania}

- [ ] **Krok 1: Test** — {pełny kod testu}

- [ ] **Krok 2: Uruchom test**

Uruchom: `{komenda}`
Oczekiwany wynik: {FAIL z powodem}

- [ ] **Krok 3: Kod** — {pełny kod}

- [ ] **Krok 4: Uruchom test**

Uruchom: `{komenda}`
Oczekiwany wynik: PASS

- [ ] **Krok 5: Commit**

```bash
git add {pliki}
git commit -m "{typ}({zakres}): {opis} (#{n})"
```
````

Zasady:

- Jeden krok to jedna czynność, do kilku minut.
- Wartości bierz ze specyfikacji: nazwy, ścieżki, teksty. Nie parafrazuj ich.
- Żadnych „TBD”, „zrób podobnie jak wyżej”, „obsłuż błędy”. Krok podaje kod albo komendę.
- Test idzie przed kodem. Każda komenda ma oczekiwany wynik.
- Plan ma linię `Issue: #<n>` i link do specyfikacji.
