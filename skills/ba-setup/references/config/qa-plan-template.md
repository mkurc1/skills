# Szablon planu testów

Plan testów opisuje scenariusze przeglądarkowe jednej zmiany. Plik `YYYY-MM-DD-slug-qa.md` leży obok specyfikacji, w `.ai/specs/` albo `.ai/specs/implemented/`. Slug jest ten sam co w specyfikacji.

````markdown
# {Tytuł} — plan testów

Dotyczy issue #{n}.

Specyfikacja: [`{YYYY-MM-DD-slug}.md`]({YYYY-MM-DD-slug}.md)

## Zakres zmiany

{Co zmienia specyfikacja, 1-3 zdania. Lista dotkniętych tras albo ekranów.}

## Scenariusze

### S{k}: {nazwa}

- **Konto:** {rola konta testowego albo „bez logowania”}
- **Zapisuje dane:** {tak albo nie}
- **Dane startowe:** {co musi istnieć, także stan zostawiony przez inny scenariusz} — `{ścieżka:linia}`
- **Kroki:**
  1. {Działanie użytkownika, z trasą i nazwą przycisku} — `{ścieżka:linia}`
- **Oczekiwany wynik:** {co widzi użytkownik} — `{ścieżka specyfikacji:linia}`

## Scenariusze bez oczekiwania w specyfikacji

- S{k}: {czego specyfikacja nie mówi}. Werdykt z góry: BLOCKED, brak informacji w specyfikacji.

## Scenariusze z działaniem zakazanym

- S{k}: {które działanie zakazane}. Werdykt z góry: BLOCKED, działanie zakazane.
````

Zasady:

- Oczekiwany wynik pochodzi ze specyfikacji, nigdy z kodu.
- Specyfikacja nie mówi, co ma się stać? Scenariusz idzie do sekcji „Scenariusze bez oczekiwania w specyfikacji”.
- Trasa, przycisk i dane startowe cytują linię kodu.
- Scenariusz, który tworzy, zmienia albo usuwa dane, ma `Zapisuje dane: tak`.
