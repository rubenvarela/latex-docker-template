# src/chapters/ - Document Chapters

This directory contains individual chapter/section files for the document.

## Purpose

Organize document content into modular, manageable files.

## Structure

```
chapters/
├── 00-introduction.tex
├── 01-chapter-name.tex
├── 02-chapter-name.tex
└── ...
```

## Naming Convention

- **Number prefix**: Two-digit number for ordering (00, 01, 02, ...)
- **Descriptive name**: Lowercase with hyphens
- **Extension**: Always `.tex`

Examples:
- `00-introduction.tex`
- `01-literature-review.tex`
- `02-methodology.tex`
- `03-results.tex`
- `04-discussion.tex`
- `05-conclusion.tex`

## File Structure

Each chapter file should:

```latex
% =============================================================================
% NN-chapter-name.tex - Chapter Title
% =============================================================================

\section{Chapter Title}
\label{sec:chapter-name}

Introduction paragraph...

\subsection{First Subsection}
\label{subsec:first}

Content...

\subsection{Second Subsection}
\label{subsec:second}

More content...

% =============================================================================
% End of NN-chapter-name.tex
% =============================================================================
```

## Including Chapters

In `src/main.tex`, include chapters in order:

```latex
\input{chapters/00-introduction}
\input{chapters/01-chapter-name}
\input{chapters/02-chapter-name}
```

## Labels

Use consistent label prefixes:
- `sec:` for sections
- `subsec:` for subsections
- `fig:` for figures within the chapter
- `tab:` for tables within the chapter
- `eq:` for equations

## Adding a New Chapter

1. Create file: `NN-chapter-name.tex`
2. Add section structure with labels
3. Include in `main.tex`
4. Rebuild: `make build`

## Best Practices

- One logical chapter per file
- Use descriptive section titles
- Add labels for cross-referencing
- Comment complex sections
- Keep consistent formatting
