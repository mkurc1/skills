# Pułapki narzędzi testów

Narzędzie z pamięcią podręczną może uruchomić test na starym kodzie. Mutacja wtedy „nie działa”, a test przechodzi. Polecenie w `project.md` § „Pojedynczy test” ma tę pamięć omijać.

Poniżej dwa przykłady. Każde narzędzie z pamięcią wyników albo kompilacji ma tę samą klasę pułapki. Sprawdź jego dokumentację, zanim wpiszesz polecenie do `project.md`.

## Python: stary `.pyc`

Python uznaje `.pyc` za aktualny, gdy zgadza się rozmiar źródła i czas zmiany w pełnych sekundach.

- Mutacja `0.5` → `0.3` nie zmienia rozmiaru pliku.
- W tej samej sekundzie Python wczyta niezmutowany moduł. Test przejdzie.

Polecenie, które omija tę pamięć:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX="$(mktemp -d)" pytest <plik> -q
```

- Pusty `PYTHONPYCACHEPREFIX` każe szukać `.pyc` w pustym katalogu. Python kompiluje źródło od nowa.
- `PYTHONDONTWRITEBYTECODE=1` nie zaśmieca `/tmp` skompilowanymi bibliotekami.
- Samo `python -B` albo samo `PYTHONDONTWRITEBYTECODE=1` nie wystarcza. Oba zabraniają zapisu, ale dalej czytają stary `.pyc` z `__pycache__`.
- Zmienne idą jako prefiks polecenia, nie przez `export`. Narzędzie powłoki agenta nie przenosi zmiennych między wywołaniami.

## vitest: ucięty werdykt

`vitest run <plik>` uruchamia jeden plik. Ścieżka działa jako filtr.

- `tail -3` na wyniku potrafi uciąć werdykt `Test Files failed`.
- Nieudana mutacja wygląda wtedy jak sukces.
- Filtruj wynik po `Tests|Test Files|FAIL`, nie po ostatnich liniach.
