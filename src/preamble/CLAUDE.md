# src/preamble/ - LaTeX Preamble Configuration

This directory contains LaTeX preamble files that configure the document.

## Purpose

Organize document configuration into modular, maintainable files.

## Files

| File | Purpose |
|------|---------|
| `packages.tex` | Package imports with options |
| `settings.tex` | Document settings (headers, paths, etc.) |
| `commands.tex` | Custom commands and environments |

## packages.tex

Contains all `\usepackage` commands organized by category:
- Document Structure: geometry, fancyhdr, titlesec, parskip
- Mathematics: amsmath, amssymb, mathtools, amsthm
- Graphics: graphicx, tikz, pgfplots, subcaption, float
- Tables: booktabs, longtable, multirow
- References: biblatex, hyperref, cleveref
- Typography: fontenc, microtype, xcolor
- Code: listings, minted

**To add a package**: Add to the appropriate category section.

## settings.tex

Document-wide settings:
- Header/footer configuration (fancyhdr)
- Section title formatting (titlesec)
- Float placement settings
- Graphics paths
- Cross-reference names (cleveref)
- Bibliography file paths

**To modify**: Edit the relevant section.

## commands.tex

Custom LaTeX commands and environments:
- Theorem environments (theorem, lemma, definition, etc.)
- Math shortcuts (number sets, operators)
- Text shortcuts (ie, eg, code)
- Utility commands (todo, note)

**To add a command**: Add to the appropriate section with a comment.

## Loading Order

In `main.tex`, these are loaded in order:
```latex
\input{preamble/packages}   % First - load packages
\input{preamble/settings}   % Second - configure packages
\input{preamble/commands}   % Third - define commands
```

## Conventions

- Group related settings together
- Add comments explaining non-obvious settings
- Use `% ===` dividers between sections
- Document package options inline
