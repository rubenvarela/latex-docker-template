# Project Structure

This document explains the organization of the LaTeX template repository.

## Directory Overview

```
latex-template/
├── src/                    # LaTeX source files (all document content)
│   └── assets/             # Images and figures
├── styles/                 # Custom style files
├── scripts/                # Build automation scripts
├── tests/                  # Test documents
├── docs/                   # Documentation
├── build/                  # Compiled output (gitignored)
├── .github/                # GitHub configuration
├── Makefile                # Build commands
├── CLAUDE.md               # AI assistant context
└── README.md               # Project overview
```

## Source Files (`src/`)

All document content lives here. Editors can focus on just this directory.

```
src/
├── main.tex              # Document entry point
├── preamble/             # Configuration
│   ├── packages.tex      # Package imports
│   ├── settings.tex      # Document settings
│   └── commands.tex      # Custom macros
├── chapters/             # Document content
│   └── 00-introduction.tex
├── bibliography/         # References
│   └── references.bib
└── assets/               # Images and figures
    ├── images/           # Raster images (PNG, JPG, PDF)
    └── figures/          # TikZ/vector graphics
```

### `main.tex`

The main file that ties everything together. It:
- Sets the document class
- Inputs preamble files
- Defines title/author
- Includes chapters
- Prints bibliography

### `preamble/`

Configuration files loaded before the document body:

| File | Purpose |
|------|---------|
| `packages.tex` | All package imports with options |
| `settings.tex` | Header/footer, spacing, graphics paths |
| `commands.tex` | Custom commands, theorem environments |

### `chapters/`

Individual chapter/section files. Naming convention:
- `00-introduction.tex` - Introduction
- `01-chapter-name.tex` - First chapter
- `02-chapter-name.tex` - Second chapter

### `bibliography/`

BibLaTeX bibliography files. Add your references to `references.bib`.

## Assets (`src/assets/`)

External resources used in the document. Located inside `src/` so editors can work with all document content in one directory.

```
src/assets/
├── images/              # Raster images (PNG, JPG, PDF)
├── figures/             # TikZ/vector graphics source
└── CLAUDE.md
```

### Images vs Figures

- **images/**: Final images ready to include
- **figures/**: Source files for generated graphics

## Styles (`styles/`)

Custom LaTeX style files (`.sty`).

```
styles/
├── template.sty         # Main template style
└── CLAUDE.md
```

Use for:
- Color palette definitions
- Custom environments
- Reusable formatting

## Scripts (`scripts/`)

Python build automation scripts using uv.

```
scripts/
├── setup.py            # Environment setup
├── build.py            # Document compilation
├── clean.py            # Artifact cleanup
├── test.py             # CI testing with act
├── watch.py            # Auto-rebuild on changes
└── CLAUDE.md
```

All scripts are self-contained with inline dependencies via uv.

## Tests (`tests/`)

Test documents for verification.

```
tests/
├── test_document.tex    # Comprehensive package test
├── fixtures/            # Test assets
└── CLAUDE.md
```

The test document exercises ALL packages to verify they work.

## Build Output (`build/`)

Compiled PDFs and auxiliary files. This directory is gitignored.

```
build/
├── main.pdf            # Compiled document
├── main.log            # Build log
├── main.aux            # Auxiliary file
└── ...                 # Other build artifacts
```

## GitHub Configuration (`.github/`)

CI/CD and GitHub-specific files.

```
.github/
├── workflows/
│   └── build.yml       # Build automation workflow
└── scripts/            # CI-only scripts (if needed)
```

## Configuration Files

| File | Purpose |
|------|---------|
| `Makefile` | Build command definitions |
| `.latexmkrc` | LaTeX build configuration |
| `.gitignore` | Git ignore patterns |
| `.actrc` | Local CI testing config |
| `Dockerfile` | Container build environment |
| `pyproject.toml` | Python project metadata |

## CLAUDE.md Files

Each directory contains a `CLAUDE.md` file that provides:
- Directory purpose
- File naming conventions
- How to extend/modify
- Related documentation

These files help AI assistants understand the project structure.

## File Naming Conventions

### LaTeX Files
- Lowercase with hyphens: `chapter-name.tex`
- Number prefix for ordering: `01-introduction.tex`
- Descriptive names: `packages.tex`, `settings.tex`

### Scripts
- Lowercase with underscores: `setup.py`, `build.py`
- Match Makefile targets: `clean.py` → `make clean`

### Documentation
- Number prefix for reading order: `01-getting-started.md`
- Lowercase with hyphens: `project-structure.md`
