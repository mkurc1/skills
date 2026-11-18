# Diagramy procesu

Ten katalog trzyma diagramy z sekcji „Proces” w głównym `README.md`. Każdy diagram ma źródło Mermaid (`.mmd`) i wyrenderowany obraz (`.png`).

## Zmiana diagramu

1. Zmień plik `.mmd`.
2. Wyrenderuj obraz:

   ```bash
   npx -y @mermaid-js/mermaid-cli@11 -i docs/diagrams/<nazwa>.mmd -o docs/diagrams/<nazwa>.png -b white -s 2 -w 1600
   ```

3. Obejrzyj obraz i zacommituj oba pliki razem.

Białe tło zostaje celowo. Obraz jest czytelny w jasnym i ciemnym motywie GitHuba.
