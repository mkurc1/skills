# Reguły review kodu

Ten plik zbiera reguły review dla projektu. To jedyne miejsce wag uwag, kolejności sprawdzania i pytań do diffu.

Czytają go:

- lokalna pętla review w skillu `ba-ship-pr`;
- recenzent PR-a.

Źródłem reguł jest `AGENTS.md`, razem z `.ai/config/` i testami kontraktów w `tests/`. Ten plik zamienia je na pytania do diffu.

## Wagi uwag

Każda uwaga ma jedną z dwóch wag.

- 🔴 **Blokująca.** Błąd w logice, brakujący przypadek, brak testu zmienionej logiki, złamana reguła projektu, ryzyko bezpieczeństwa.
- 🟡 **Drobna.** Styl, nazewnictwo, prostszy zapis, sugestia poza zakresem PR-a.

Werdykt zależy tylko od uwag blokujących. Zero blokujących to approve.

Błąd spoza zakresu PR-a nie wpływa na werdykt. Recenzent zgłasza go według [`project.md` § Zgłaszanie błędów spoza zakresu](project.md#zgłaszanie-błędów-spoza-zakresu).

## Kolejność sprawdzania

1. Poprawność logiki i brakujące przypadki.
2. Bezpieczeństwo.
3. Testy zmienionej logiki.
4. Dokumentacja.

## Pytania do diffu

### Jedna reguła w jednym miejscu

Ten sam warunek w drugim pliku to uwaga blokująca. Sygnały:

- Parametr przechodzi przez kilka warstw opakowań.
- Zabezpieczenie stoi u wywołujących, a nie w wołanej metodzie.
- Pominięcie jednego miejsca niczego nie psuje widocznie.

### Architektura

- Skill woła inny skill tylko przez jego sekcję `## Wywołanie`. Odwołanie do sekcji albo kroku innego skilla blokuje PR.
- Skill nie nazywa projektu, w którym powstał. Fakty o projekcie stoją w `.ai/config/`.
- Kod na zapas jest uwagą. Przykłady: interfejs z jedną implementacją, opcja bez czytelnika, parametr z tą samą wartością u wszystkich.

### Bezpieczeństwo

- Sekret albo klucz w diffie blokuje PR.
- Endpoint chroniony sprawdza autoryzację. Endpoint administratora wymaga roli administratora.
- Wejście z zewnątrz przechodzi walidację.
- Zapytanie w pętli (N+1) albo filtr bez indeksu na dużej tabeli to uwaga.

### Testy

- Zmieniona logika ma test, który pada bez zmiany. Dowodem jest weryfikacja mutacyjna.

### Dokumentacja

- Zmiana zachowania aktualizuje dokumentację w tym samym PR-ze.
- Dokumentacja i treść skilli są po polsku, z pełną diakrytyką.
- Zrobiona specyfikacja przechodzi do `.ai/specs/implemented/`.

## Czego review nie sprawdza

Lint, typy i testy to osobne checki bramki jakości. Recenzent nie prosi o ich potwierdzenie.
