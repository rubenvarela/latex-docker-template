# src/ - LaTeX Source Files

This directory contains all document content. Editors can focus on just this directory.

## Purpose

Houses all LaTeX content organized in a modular structure, including assets.

## Structure

```
src/
├── main.tex              # Document entry point
├── preamble/             # Configuration (packages, settings, commands)
├── chapters/             # Document content
├── bibliography/         # BibLaTeX files
└── assets/               # Images and figures
    ├── images/           # Raster images (PNG, JPG, PDF)
    └── figures/          # TikZ/vector graphics
```

## Key Files

### main.tex

The main document entry point that:
- Sets document class and options
- Inputs preamble files
- Defines document metadata (title, author, date)
- Includes chapter files
- Prints bibliography

**To compile**: `make build` (compiles this file)

### preamble/

Configuration files loaded before `\begin{document}`:
- `packages.tex` - All package imports
- `settings.tex` - Document settings (headers, spacing, paths)
- `commands.tex` - Custom commands and theorem environments

### chapters/

Individual chapter/section files:
- Named with number prefix: `00-introduction.tex`, `01-methods.tex`
- Each file contains one logical section
- Included in `main.tex` with `\input{chapters/filename}`

### bibliography/

BibLaTeX bibliography files:
- `references.bib` - Main bibliography database
- Additional `.bib` files can be added

### assets/

Images and figures for the document:
- `images/` - Raster images (PNG, JPG, PDF) ready to include
- `figures/` - TikZ/vector graphics source files

Use `\includegraphics{filename}` - the graphicspath is configured in `settings.tex`.

## Conventions

- **File naming**: Lowercase with hyphens, number prefix for ordering
- **Labels**: Use descriptive labels like `sec:introduction`, `fig:diagram`
- **Comments**: Add `% ===` section dividers for clarity
- **Modular**: One concept per file where practical

## Building

```bash
make build        # Full build
make build-draft  # Quick draft (single pass)
make watch        # Auto-rebuild on changes
```

## Adding Content

1. Create new chapter: `chapters/NN-chapter-name.tex`
2. Add content with sections/subsections
3. Include in `main.tex`: `\input{chapters/NN-chapter-name}`
4. Rebuild: `make build`
