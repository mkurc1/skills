# Reguły review kodu

Ten plik zbiera reguły review dla projektu. To jedyne miejsce wag uwag, kolejności sprawdzania i pytań do diffu.

Czytają go:

- lokalna pętla review w skillu `ba-ship-pr`;
<!-- ba-setup: wariant review-ai -->
- review AI w CI: {link do jego opisu};
<!-- ba-setup: koniec wariantu -->
- recenzent PR-a.

Źródłem reguł jest {plik z regułami pracy agenta, na przykład `AGENTS.md`}. Ten plik zamienia je na pytania do diffu.

## Wagi uwag

Każda uwaga ma jedną z dwóch wag.

- 🔴 **Blokująca.** Błąd w logice, brakujący przypadek, brak testu zmienionej logiki, złamana reguła projektu, ryzyko bezpieczeństwa.
- 🟡 **Drobna.** Styl, nazewnictwo, prostszy zapis, sugestia poza zakresem PR-a.

Werdykt zależy tylko od uwag blokujących. Zero blokujących to approve.

Błąd spoza zakresu PR-a nie wpływa na werdykt. Recenzent zgłasza go według [`project.md` § Zgłaszanie błędów spoza zakresu](project.md#zgłaszanie-błędów-spoza-zakresu).

## Kolejność sprawdzania

1. Poprawność logiki i brakujące przypadki.
2. Reguły domeny.
3. Bezpieczeństwo.
4. Testy zmienionej logiki.
5. Dokumentacja.

## Pytania do diffu

### Reguły domeny

{Reguły domeny projektu z wywiadu, po jednym pytaniu do diffu. Na przykład: brak danych daje pustą wartość, nie zero. Usuń podsekcję i punkt 2 kolejności, gdy brak.}

### Jedna reguła w jednym miejscu

Ten sam warunek w drugim pliku to uwaga blokująca. Sygnały:

- Parametr przechodzi przez kilka warstw opakowań.
- Zabezpieczenie stoi u wywołujących, a nie w wołanej metodzie.
- Pominięcie jednego miejsca niczego nie psuje widocznie.

### Architektura

- {Narzędzie granic modułów: import łamiący jego reguły blokuje PR, wyjątek dopisuje tylko człowiek. Usuń punkt, gdy repo go nie ma.}
- {Inne reguły architektury projektu, na przykład granica transakcji albo kształt endpointu.}
- Kod na zapas jest uwagą. Przykłady: interfejs z jedną implementacją, opcja bez czytelnika, parametr z tą samą wartością u wszystkich.

### Konwencje kodu

{Konwencje kodu projektu: język kodu i komentarzy, zakazane wywołania, nazewnictwo. Usuń podsekcję, gdy brak.}

### Bezpieczeństwo

- Sekret albo klucz w diffie blokuje PR.
- Endpoint chroniony sprawdza autoryzację. Endpoint administratora wymaga roli administratora.
- Wejście z zewnątrz przechodzi walidację.
- Zapytanie w pętli (N+1) albo filtr bez indeksu na dużej tabeli to uwaga.
- {Reguły bezpieczeństwa projektu, na przykład dozwolone zmienne w kodzie przeglądarki. Usuń punkt, gdy brak.}

### Baza i migracje

- {Gdzie leżą migracje i jakim narzędziem powstają. Usuń podsekcję, gdy repo nie ma bazy.}
- Polecenie kasujące dane albo całą bazę bez polecenia użytkownika to uwaga blokująca.

### Testy

- Zmieniona logika ma test, który pada bez zmiany. Dowodem jest weryfikacja mutacyjna.
- {Ścieżki, których zmiana wymaga w opisie PR-a dowodu drugą drogą. Usuń punkt, gdy brak.}

### Dokumentacja

- Zmiana zachowania aktualizuje dokumentację w tym samym PR-ze.
- {Język i zasady pisania dokumentacji projektu.}
- Zrobiona specyfikacja przechodzi do `.ai/specs/implemented/`.

## Czego review nie sprawdza

Lint, typy i testy to osobne checki bramki jakości. Recenzent nie prosi o ich potwierdzenie.
