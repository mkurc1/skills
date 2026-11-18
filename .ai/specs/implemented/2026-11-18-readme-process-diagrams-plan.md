# Diagramy procesu skilli ba-* w README — plan implementacji

Issue: #4

**Cel:** README ma sekcję `## Proces` z 4 diagramami PNG i opisem flow pod każdym.

**Architektura:** Źródła Mermaid i PNG leżą w `docs/diagrams/`. Najpierw test, który pilnuje osadzenia obrazów. Potem diagramy, na końcu sekcja README.

Specyfikacja: [`.ai/specs/2026-11-18-readme-process-diagrams.md`](2026-11-18-readme-process-diagrams.md)

## Ograniczenia globalne

- Nazwy plików: `01-dwie-drogi`, `02-fix-issue-tory`, `03-decyzje-operatora`, `04-klocki-i-lancuchy`.
- Render: `npx -y @mermaid-js/mermaid-cli@11 -i <plik>.mmd -o <plik>.png -b white -s 2 -w 1600`.
- Bez nowej zależności w `pyproject.toml` i bez zmian w CI.
- Treść diagramów bierzesz z `SKILL.md` i `.ai/config/project.md`, nie z artykułu.
- Teksty w diagramach po polsku, z pełną diakrytyką.

## Na co uważać

- **Znaki specjalne Mermaid.** `#`, `<` i `>` w etykietach psują render albo znikają. Task 2 ogląda każdy PNG.
- **Czytelność.** Diagram za szeroki staje się nieczytelny w README. Task 2 sprawdza szerokość PNG i tekst na obrazie.

---

### Task 1: Test osadzenia diagramów

**Pliki:**
- Utwórz: `tests/test_readme_diagrams.py`

**Interfejsy:**
- Dostarcza: test, który Task 3 zazielenia.

- [ ] **Krok 1: Test**

```python
"""README embeds the process diagrams, and every diagram keeps its Mermaid source."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
DIAGRAMS_DIR = ROOT / "docs" / "diagrams"
DIAGRAMS = [
    "01-dwie-drogi",
    "02-fix-issue-tory",
    "03-decyzje-operatora",
    "04-klocki-i-lancuchy",
]
IMAGE = re.compile(r"!\[[^\]]+\]\((docs/diagrams/[^)]+\.png)\)")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def test_readme_embeds_every_diagram_in_order() -> None:
    embedded = IMAGE.findall(README.read_text(encoding="utf-8"))

    assert embedded == [f"docs/diagrams/{name}.png" for name in DIAGRAMS]


@pytest.mark.parametrize("name", DIAGRAMS)
def test_diagram_has_source_and_png(name: str) -> None:
    assert (DIAGRAMS_DIR / f"{name}.mmd").is_file()
    assert (DIAGRAMS_DIR / f"{name}.png").read_bytes()[:8] == PNG_SIGNATURE
```

- [ ] **Krok 2: Uruchom test**

Uruchom: `uv run pytest tests/test_readme_diagrams.py`
Oczekiwany wynik: FAIL. README nie osadza obrazów, plików diagramów nie ma.

- [ ] **Krok 3: Commit**

```bash
git add tests/test_readme_diagrams.py
git commit -m "test(readme): pilnuje osadzenia diagramów procesu (#4)"
```

### Task 2: Diagramy Mermaid i PNG

**Pliki:**
- Utwórz: `docs/diagrams/01-dwie-drogi.mmd`, `02-fix-issue-tory.mmd`, `03-decyzje-operatora.mmd`, `04-klocki-i-lancuchy.mmd`
- Utwórz: te same nazwy z `.png`

**Interfejsy:**
- Wymaga: nic.
- Dostarcza: 4 PNG dla Task 3.

- [ ] **Krok 1: `01-dwie-drogi.mmd`**

```
flowchart LR
  classDef stage fill:#e8f0fe,stroke:#3b6fd6,color:#1a1a1a
  classDef human fill:#fff4d6,stroke:#b8860b,color:#1a1a1a
  classDef result fill:#e6f4ea,stroke:#2e8b57,color:#1a1a1a

  subgraph FIX["/ba-fix-issue"]
    direction LR
    F1["1. Start<br/>ba-github-issues start"] --> F2["2. Specyfikacja i plan<br/>ba-plan"] --> F3["3. Implementacja<br/>ba-implement"] --> F4["4. Wysyłka<br/>ba-ship-pr + ba-wait-checks"]
  end
  subgraph AUTO["/ba-auto-fix-issue"]
    direction LR
    A1["1. Start<br/>ba-github-issues start"] --> A2["2. Specyfikacja i plan<br/>ba-plan --auto"] --> A3["3. Implementacja<br/>ba-implement"] --> A4["4. Wysyłka<br/>ba-ship-pr + ba-wait-checks"]
  end

  OF(["Operator: rozmowa,<br/>wybór podejścia, akceptacja specyfikacji"]) -.- F2
  OA(["Operator: jeden zestaw odpowiedzi"]) -.- A2
  F4 --> PR["PR z wynikiem każdego checka"]
  A4 --> PR
  PR --> M(["Człowiek: review i merge"])
  STOP(["Start, Implementacja, Wysyłka:<br/>operator tylko przy zatrzymaniu"])

  class F1,F2,F3,F4,A1,A2,A3,A4 stage
  class OF,OA,M,STOP human
  class PR result
```

- [ ] **Krok 2: `02-fix-issue-tory.mmd`**

```
sequenceDiagram
  autonumber
  actor O as Operator
  participant A as Agent
  participant G as GitHub

  O->>A: /ba-fix-issue n
  A->>G: ba-github-issues read: treść i komentarze
  A->>G: ba-github-issues start: in-progress, assignee, gałąź
  rect rgb(255, 244, 214)
    note over O,A: ba-plan, rozmowa o specyfikacji
    A->>O: pytania po jednym, 2–3 podejścia
    O->>A: odpowiedzi i wybór podejścia
    A->>O: specyfikacja do akceptacji
    O->>A: akceptuję
  end
  A->>A: plan w .ai/specs/
  A->>G: komentarz z planem w issue
  A->>A: ba-implement: zadania z planu, bramka jakości, commit
  A->>A: ba-ship-pr: bramka jakości, lokalne review
  A->>G: push i PR z „Closes” do issue
  A->>G: ba-wait-checks: czeka na każdy check
  G-->>A: wynik każdego checka
  A->>O: raport końcowy z linkiem do PR-a
  O->>G: review i merge
  G->>G: issue zamknięte po merge
```

- [ ] **Krok 3: `03-decyzje-operatora.mmd`**

```
flowchart LR
  classDef decision fill:#fde8e8,stroke:#c0392b,color:#1a1a1a
  classDef moment fill:#e8f0fe,stroke:#3b6fd6,color:#1a1a1a
  classDef human fill:#fff4d6,stroke:#b8860b,color:#1a1a1a

  subgraph D["Decyzje opiekuna z .ai/config/project.md"]
    direction TB
    D1["Zmiana, która wymaga zapisu<br/>decyzji architektonicznej (ADR)"]
    D2["Zmiana granic modułów"]
    D3["Nowa biblioteka<br/>albo usługa zewnętrzna"]
    D4["Wyraźna zmiana projektu systemu"]
    D5["Zmiana kontraktu .ai/config/"]
  end

  D --> M1["Moment 1: ba-plan, strażnik nr 1<br/>decyzja trafia do pytań<br/>przed specyfikacją"]
  D --> M2["Moment 2: ba-implement, strażnik nr 2<br/>decyzja spoza specyfikacji<br/>zatrzymuje pracę"]
  M1 --> Q(["Operator wybiera opcję"])
  M2 --> Q
  Q --> S["Agent pracuje dalej z wyborem operatora"]

  class D1,D2,D3,D4,D5 decision
  class M1,M2 moment
  class Q human
```

- [ ] **Krok 4: `04-klocki-i-lancuchy.mmd`**

```
flowchart TB
  classDef chain fill:#e8f0fe,stroke:#3b6fd6,color:#1a1a1a
  classDef block fill:#e6f4ea,stroke:#2e8b57,color:#1a1a1a
  classDef side fill:#f2f2f2,stroke:#777777,color:#1a1a1a

  SETUP["ba-setup<br/>raz na repo: .ai/config/"]
  REFINE["ba-refine-issue<br/>uzupełnia niegotowe issue"]

  subgraph CH["Łańcuchy"]
    FIX["/ba-fix-issue"]
    AUTO["/ba-auto-fix-issue"]
  end

  subgraph BL["Klocki"]
    GI["ba-github-issues start"]
    PLAN["ba-plan"]
    IMPL["ba-implement"]
    SHIP["ba-ship-pr"]
    WAIT["ba-wait-checks"]
    MUT["ba-mutation-check"]
  end

  QA["ba-qa<br/>na żądanie operatora,<br/>zmiana w interfejsie"]

  SETUP -.-> REFINE -.->|issue gotowe| CH
  FIX --> GI
  FIX -->|z operatorem| PLAN
  FIX --> IMPL
  FIX --> SHIP
  AUTO --> GI
  AUTO -->|--auto| PLAN
  AUTO --> IMPL
  AUTO --> SHIP
  SHIP --> WAIT
  SHIP --> MUT
  IMPL -.->|po implementacji| QA

  class FIX,AUTO chain
  class GI,PLAN,IMPL,SHIP,WAIT,MUT block
  class SETUP,REFINE,QA side
```

- [ ] **Krok 5: Render**

Uruchom:

```bash
for f in docs/diagrams/*.mmd; do npx -y @mermaid-js/mermaid-cli@11 -i "$f" -o "${f%.mmd}.png" -b white -s 2 -w 1600; done
```

Oczekiwany wynik: 4 pliki PNG, bez błędu parsowania.

- [ ] **Krok 6: Przegląd obrazów**

Otwórz każdy PNG narzędziem Read. Sprawdź:
- tekst czytelny, polskie znaki poprawne;
- treść zgodna z sekcją „Treść diagramów” w specyfikacji;
- szerokość obrazu do około 2400 px przy skali 2.

Poprawka układu albo tekstu? Zmień `.mmd`, wyrenderuj ponownie, zapisz wybór w dzienniku.

- [ ] **Krok 7: Commit**

```bash
git add docs/diagrams/
git commit -m "docs(diagrams): 4 diagramy procesu skilli ba-* (#4)"
```

### Task 3: Sekcja `## Proces` w README

**Pliki:**
- Zmień: `README.md`, wstaw sekcję między `## Skille` a `## Testy`
- Utwórz: `docs/diagrams/README.md`

**Interfejsy:**
- Wymaga: test z Task 1, PNG z Task 2.

- [ ] **Krok 1: Sekcja README**

```markdown
## Proces

Skille składają się w proces od issue do merge'a. Źródła diagramów i sposób ich renderowania: [`docs/diagrams/`](docs/diagrams/README.md).

### Dwie drogi przez 4 etapy

![Dwa łańcuchy, /ba-fix-issue i /ba-auto-fix-issue, przechodzą te same 4 etapy: start, specyfikacja i plan, implementacja, wysyłka](docs/diagrams/01-dwie-drogi.png)

Oba łańcuchy przechodzą te same 4 etapy i kończą się PR-em z wynikiem każdego checka. Różnią się etapem specyfikacji: w `/ba-fix-issue` operator ją współtworzy i akceptuje, w `/ba-auto-fix-issue` odpowiada raz na pytania.

### `/ba-fix-issue` krok po kroku

![Kroki /ba-fix-issue w torach operator, agent i GitHub, od wywołania do merge'a](docs/diagrams/02-fix-issue-tory.png)

Operator wywołuje łańcuch i rozmawia z agentem tylko o specyfikacji. Resztę do raportu z PR-em agent robi sam, a review i merge zostają po stronie człowieka.

### Gdzie decyduje operator

![5 rodzajów decyzji opiekuna i 2 momenty, w których agent pyta: strażnik w ba-plan i strażnik w ba-implement](docs/diagrams/03-decyzje-operatora.png)

Decyzji opiekuna agent nigdy nie podejmuje sam. Pyta o nią w `ba-plan` przed specyfikacją albo staje w `ba-implement`, gdy decyzja wyjdzie dopiero w kodzie.

### Klocki i łańcuchy

![Łańcuchy /ba-fix-issue i /ba-auto-fix-issue wołają klocki ba-github-issues, ba-plan, ba-implement i ba-ship-pr, a ba-ship-pr woła ba-wait-checks i ba-mutation-check](docs/diagrams/04-klocki-i-lancuchy.png)

Łańcuch to skill, który woła klocki w ustalonej kolejności. `ba-setup` i `ba-refine-issue` działają przed łańcuchem, a `ba-qa` uruchamiasz osobno po implementacji.
```

- [ ] **Krok 2: `docs/diagrams/README.md`**

```markdown
# Diagramy procesu

Ten katalog trzyma diagramy z sekcji „Proces” w głównym `README.md`. Każdy diagram ma źródło Mermaid (`.mmd`) i wyrenderowany obraz (`.png`).

## Zmiana diagramu

1. Zmień plik `.mmd`.
2. Wyrenderuj obraz:

   ```bash
   npx -y @mermaid-js/mermaid-cli@11 -i docs/diagrams/<nazwa>.mmd -o docs/diagrams/<nazwa>.png -b white -s 2 -w 1600
   ```

3. Zacommituj oba pliki razem.

Białe tło zostaje celowo. Obraz jest czytelny w jasnym i ciemnym motywie GitHuba.
```

- [ ] **Krok 3: Uruchom test**

Uruchom: `uv run pytest tests/test_readme_diagrams.py`
Oczekiwany wynik: PASS.

- [ ] **Krok 4: Commit**

```bash
git add README.md docs/diagrams/README.md
git commit -m "docs(readme): sekcja Proces z diagramami skilli ba-* (#4)"
```

### Task 4: Bramka jakości

- [ ] **Krok 1: Bramka**

Uruchom:

```bash
uv sync --locked
uv run ruff check tests/
uv run ruff format --check tests/
uv run pytest
```

Oczekiwany wynik: każda komenda kończy się kodem 0.
