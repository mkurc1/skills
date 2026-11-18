# Wspólne ustawienia edytora i gita w repo

Issue: #11

## Cel
Repo nie ma wspólnych ustawień edytora i gita. Po zmianie `.editorconfig` ustala wcięcia i końce linii dla każdego typu pliku, a `.gitattributes` wymusza LF w gicie. `.gitignore` pomija lokalne pliki agentów.

## Zakres
- Nowy plik `.editorconfig` w katalogu głównym.
- Nowy plik `.gitattributes` w katalogu głównym.
- Dwa nowe wpisy w `.gitignore`: `CLAUDE.local.md` i `.worktrees/`.
- Nowy test `tests/test_repo_settings.py`, który pilnuje trzech plików i braku CRLF.

### Poza zakresem
- Wpis `.claude/scratch/`. Prowadzi go #7.
- Szablony issue i PR-a w `.github/`. Opis PR-a pisze `ba-ship-pr` według `.ai/config/pull-request.md`.
- `CONTRIBUTING.md`, `DECISIONS.md`, `CHANGELOG.md`.
- Zmiana istniejących plików pod nowe reguły. Pliki już je spełniają, sprawdzone niżej.

## Projekt

### `.editorconfig`
Wartości wynikają z istniejącego kodu. Żadna nie jest decyzją opiekuna.

| Wzorzec | Wcięcie | Długość linii | Źródło |
|---|---|---|---|
| `*` | — | — | wspólne: `charset = utf-8`, `end_of_line = lf`, `insert_final_newline = true`, `trim_trailing_whitespace = true` |
| `*.md` | spacje, 2 | bez limitu | listy w repo mają wcięcie 2 spacji. Proza w jednej linii na akapit |
| `*.py` | spacje, 4 | 100 | `[tool.ruff] line-length = 100` w `pyproject.toml` |
| `*.{yml,yaml}` | spacje, 2 | bez limitu | `.github/workflows/ci.yml` |
| `*.toml` | spacje, 4 | bez limitu | `pyproject.toml` |
| `*.json` | spacje, 2 | bez limitu | konwencja JSON. Repo nie ma dziś plików JSON |

- `trim_trailing_whitespace` zostaje `true` także dla Markdownu. Żaden plik `.md` nie używa dwóch spacji na końcu linii. Sprawdzone: `git grep -nE '[[:space:]]+$'` nie zwraca trafień.
- Długość linii „bez limitu” to `max_line_length = off`.
- Odrzucona alternatywa: limit 100 znaków dla Markdownu. Akapity w repo są w jednej linii, limit złamałby niemal każdy plik.

### `.gitattributes`
```
* text=auto eol=lf
*.png binary
```
- `text=auto` pozwala gitowi rozpoznać pliki tekstowe. `eol=lf` wymusza LF w drzewie roboczym na każdym systemie.
- `*.png binary` wyłącza normalizację i diff tekstowy dla `docs/diagrams/*.png`.
- Odrzucona alternatywa: lista rozszerzeń tekstowych zamiast `*`. Nowy typ pliku wypadłby spod reguły.

### `.gitignore`
Po istniejących 5 wpisach dochodzą `CLAUDE.local.md` i `.worktrees/`.

### Test
`tests/test_repo_settings.py` sprawdza:
- sekcje `.editorconfig` dla `*.md`, `*.py`, `*.{yml,yaml}`, `*.toml`, `*.json` i `max_line_length = 100` dla `*.py`;
- reguły `* text=auto eol=lf` i `*.png binary` w `.gitattributes`;
- wpisy `CLAUDE.local.md` i `.worktrees/` w `.gitignore`;
- brak plików z CRLF według `git ls-files --eol`.

## Plan
1. Test `tests/test_repo_settings.py` pada na brak plików. Sprawdza `uv run pytest tests/test_repo_settings.py`.
2. Trzy pliki konfiguracji. Test przechodzi.
3. Bramka jakości z `.ai/config/project.md`.

## Gotowe gdy
- `uv run pytest tests/test_repo_settings.py` przechodzi.
- `git ls-files --eol | grep crlf` nie zwraca trafień.
- Bramka jakości przechodzi.

## Ryzyka i otwarte pytania
- **Konflikt z #7 w `.gitignore`.** Kto merguje drugi, łączy wpisy.
- `.editorconfig` działa tylko w edytorze z jego obsługą. CI go nie sprawdza. Test pilnuje treści pliku, nie zachowania edytora.
