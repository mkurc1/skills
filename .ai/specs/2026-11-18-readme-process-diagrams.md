# Diagramy procesu skilli ba-* w README

Issue: #4

## Cel

README opisuje każdy skill osobno, ale nie pokazuje, jak skille składają się w proces od issue do merge'a. Po zmianie README ma sekcję z 4 diagramami PNG. Pod każdym diagramem stoi 1–2 zdania opisu flow.

## Zakres

- 4 diagramy w `docs/diagrams/`: źródło Mermaid `.mmd` i wyrenderowany `.png` dla każdego.
- Nowa sekcja `## Proces` w `README.md`, między tabelą `## Skille` a `## Testy`.
- Krótki akapit w `docs/diagrams/README.md`: jak przerenderować obrazy.
- Drobne zmiany istniejącego tekstu README, gdy kolidują z diagramami.

### Poza zakresem

- Diagram „Stan wdrożenia” z artykułu.
  - Szybko się starzeje i opisuje issue innego repo.
- Zmiany w treści skilli, w `.ai/config/` i w samym artykule.
- Zależność od Mermaid CLI w `pyproject.toml` albo w CI.
  - Render robi autor diagramu raz, przy zmianie.

## Decyzje operatora

| Decyzja | Wybór | Odrzucone alternatywy |
|---|---|---|
| Narzędzie | Mermaid CLI (`npx -y @mermaid-js/mermaid-cli@11`), źródło `.mmd` w repo obok PNG | Mermaid bez źródła w repo: zmiana wymaga rysowania od nowa. Ręczny SVG/HTML: trudny w utrzymaniu. |
| Katalog i nazwy | `docs/diagrams/NN-nazwa.{mmd,png}`, numer = kolejność w README | `.github/assets/`: mniej widoczny. `.ai/docs/diagrams/`: miesza się z plikami, które `ba-setup` daje innym repo. |
| Ciemny motyw | Jeden PNG na diagram, białe nieprzezroczyste tło | Dwa warianty z `<picture>`: 8 obrazów do utrzymania. Przezroczyste tło: ciemne linie giną na ciemnym tle. |

Mermaid CLI to narzędzie autora, nie zależność projektu. Operator zatwierdził je jako decyzję opiekuna z sekcji „Decyzje opiekuna” w `.ai/config/project.md`.

## Projekt

### Pliki

| Plik | Diagram |
|---|---|
| `docs/diagrams/01-dwie-drogi.mmd` / `.png` | Dwie drogi przez 4 etapy |
| `docs/diagrams/02-fix-issue-tory.mmd` / `.png` | `/ba-fix-issue` krok po kroku w torach |
| `docs/diagrams/03-decyzje-operatora.mmd` / `.png` | Gdzie decyduje operator |
| `docs/diagrams/04-klocki-i-lancuchy.mmd` / `.png` | Klocki i łańcuchy |

Render: `npx -y @mermaid-js/mermaid-cli@11 -i <plik>.mmd -o <plik>.png -b white -s 2 -w 1600`. Skala 2 daje ostry obraz na ekranach o dużej gęstości. Szerokość okna 1600 px chroni szeroki diagram przed zmniejszeniem.

README osadza obraz ścieżką względną: `![opis](docs/diagrams/01-dwie-drogi.png)`. Tekst alternatywny streszcza diagram.

### Treść diagramów

Źródłem prawdy są pliki `SKILL.md`, `.ai/config/project.md` i `.ai/docs/sdlc.md`. Nie artykuł.

1. **Dwie drogi.** 4 etapy: Start (`ba-github-issues start`), Specyfikacja i plan (`ba-plan`), Implementacja (`ba-implement`), Wysyłka (`ba-ship-pr` + `ba-wait-checks`).
   - `/ba-fix-issue`: operator prowadzi rozmowę o specyfikacji i ją akceptuje.
   - `/ba-auto-fix-issue`: operator odpowiada raz na zestaw pytań `ba-plan --auto`.
   - W obu drogach Start, Implementacja i Wysyłka pytają operatora tylko przy zatrzymaniu.
   - Po PR-ze: review i merge robi człowiek.
2. **`/ba-fix-issue` w torach** operator, agent, GitHub.
   - Agent: odczyt, start, rozmowa, specyfikacja, plan, implementacja, bramka jakości, lokalne review, push, czekanie na checki.
   - Operator: wywołanie, odpowiedzi w rozmowie, akceptacja specyfikacji, review i merge.
   - GitHub: etykieta `in-progress` i assignee, gałąź, komentarz z planem, PR, checki, zamknięcie issue przez `Closes #n` po merge.
3. **Gdzie decyduje operator.**
   - 5 rodzajów decyzji opiekuna z `.ai/config/project.md`: ADR, granice modułów, nowa biblioteka albo usługa, wyraźna zmiana projektu systemu, zmiana kontraktu `.ai/config/`.
   - Moment 1: strażnik nr 1 w `ba-plan`. Decyzja opiekuna zawsze trafia do pytań przed specyfikacją.
   - Moment 2: strażnik nr 2 w `ba-implement`. Decyzja opiekuna spoza specyfikacji zatrzymuje pracę.
4. **Klocki i łańcuchy.**
   - `ba-fix-issue` i `ba-auto-fix-issue` wołają `ba-github-issues`, `ba-plan` (z `--auto` w drugim łańcuchu), `ba-implement`, `ba-ship-pr`.
   - `ba-ship-pr` woła `ba-wait-checks` i `ba-mutation-check`.
   - Przed łańcuchem: `ba-setup` raz na repo, `ba-refine-issue` dla niegotowego issue.
   - Poza łańcuchem, na żądanie: `ba-qa` po implementacji zmiany w interfejsie.

## Plan

1. Napisać 4 pliki `.mmd` — render bez błędów Mermaid CLI.
2. Wyrenderować 4 PNG — pliki istnieją, mają białe tło.
3. Obejrzeć każdy PNG — tekst czytelny, zgodny z „Treścią diagramów”.
4. Dodać sekcję `## Proces` do README i `docs/diagrams/README.md`.
5. Bramka jakości — zielona.

## Gotowe gdy

- `docs/diagrams/` ma 4 pary `.mmd` i `.png`.
- `README.md` osadza 4 obrazy, pod każdym 1–2 zdania opisu flow.
- Diagram 4 wymienia wszystkie 9 klocków z issue.
- Diagram 3 wymienia 5 decyzji opiekuna i 2 momenty pytania.
- Diagramy 1 i 2 pokazują czekanie na checki przez `ba-wait-checks`.
- Obrazy renderują się w podglądzie README na GitHubie. Sprawdzenie: widok pliku na gałęzi PR-a.
- Bramka jakości z `.ai/config/project.md` przechodzi.

## Ryzyka i otwarte pytania

- Mermaid CLI pobiera przeglądarkę przy pierwszym uruchomieniu. Lokalnie render działa.
- Diagramy mogą się zestarzeć przy zmianie skilli.
  - Źródło `.mmd` w repo obniża koszt poprawki.
