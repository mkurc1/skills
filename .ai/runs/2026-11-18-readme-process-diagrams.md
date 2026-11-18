# Dziennik: diagramy procesu skilli ba-* w README

Issue: #4
Plan: [`.ai/specs/implemented/2026-11-18-readme-process-diagrams-plan.md`](../specs/implemented/2026-11-18-readme-process-diagrams-plan.md)

## Wybory

- Plan wykonuję sam w głównej sesji, zadanie po zadaniu, zamiast podagenta na zadanie.
  - Powód: 3 małe zadania dokumentacyjne. Task 2 wymaga oglądania PNG i poprawek układu w pętli.
  - Recenzja całej gałęzi idzie do osobnego agenta.
- Render z `-w 1600`. Domyślne okno 800 px zmniejszało szeroki diagram 1 do nieczytelnego tekstu. Spec i plan poprawione.
- Diagramy z nagłówkiem `config: flowchart: wrappingWidth`. Domyślne zawijanie łamało nazwy skilli w połowie (`ba-wait-` / `checks`).
- Diagram 1 w układzie pionowym: dwie kolumny łańcuchów. Układ poziomy miał 3168 px i za mały tekst.
  - Uwaga „Start, Implementacja i Wysyłka pytają operatora tylko przy zatrzymaniu” przeszła do opisu pod diagramem. Jako osobny węzeł wisiała bez połączeń.
- Diagram 3: 5 decyzji w jednym bloku z listą. Osobne bloki dawały obraz 1940 px wysokości.
- Diagram 4: klocki w kolejności wywołania, jedna strzałka z łańcuchów. 8 krzyżujących się strzałek było nieczytelne.

## Postęp

- Task 1: test `tests/test_readme_diagrams.py`, 5 czerwonych. Commit b62893a.
- Task 2: 4 pary `.mmd` + `.png`, każdy PNG obejrzany.
- Task 3: sekcja `## Proces` w README i `docs/diagrams/README.md`. Test zielony.
- Weryfikacja: bramka jakości zielona, 81 testów. Mutacja testu: zła ścieżka w README i brak `.mmd` dają czerwień.
- Druga droga: grep źródeł `.mmd` (9 klocków, 5 decyzji, `ba-wait-checks` w diagramach 1 i 2), PNG w trybie RGB bez przezroczystości.
- Recenzja całej gałęzi (osobny agent): 5 uwag, wszystkie przyjęte.
  - Diagram 1: adnotacja „operator tylko przy zatrzymaniu” w etapach 1, 3, 4. Wraca wymóg ze specyfikacji.
  - Diagram 4: strzałka `ba-implement` → `ba-mutation-check` według „Dobór skilli” w `project.md`.
  - README: podpis diagramu 2 bez „tylko o specyfikacji”, `--auto` bez „raz”, zgoda zaimka w podpisie diagramu 3.
- ba-ship-pr: bramka zielona, lokalne review (security, quality, docs) bez znalezisk w rundzie 1.
- Specyfikacja i plan przeniesione do `.ai/specs/implemented/`.
