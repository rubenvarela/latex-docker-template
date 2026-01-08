# LaTeX Template Repository

A comprehensive template for building LaTeX documents with modern tooling, CI/CD automation, and best practices.

## Project Overview

This is a template repository for building LaTeX documents with:
- **Docker-first builds** - No local LaTeX installation required!
- **GitHub Actions** workflow for automated PDF builds
- **Python/uv** scripts for build automation
- **Modular structure** for maintainable documents

**All builds run inside Docker** using `texlive/texlive:latest-full`. Users only need Docker installed - no local TeX Live setup required.

## Directory Structure

```
├── src/                    # LaTeX source files (all document content)
│   ├── main.tex           # Document entry point
│   ├── preamble/          # Packages, settings, commands
│   ├── chapters/          # Document chapters
│   ├── bibliography/      # BibLaTeX files
│   └── assets/            # Images and figures
│       ├── images/        # Raster images (PNG, JPG, PDF)
│       └── figures/       # TikZ/vector graphics
├── styles/                # Custom .sty files
├── scripts/               # Python/uv build scripts
├── tests/                 # Test documents
├── docs/                  # User documentation
├── build/                 # Output directory (gitignored)
└── .github/workflows/     # CI/CD configuration
```

## Quick Commands

```bash
make setup        # Check Docker and pull TeX Live image
make init         # Interactive wizard to customize template
make build        # Compile document (Docker)
make build-draft  # Quick draft build (Docker)
make watch        # Auto-rebuild on changes (Docker)
make test         # Run CI locally with act
make clean        # Remove artifacts
make docker-shell # Open shell in LaTeX container
make build-local  # Build with local LaTeX (no Docker)
make help         # Show all commands
```

## Included Packages

**Document Structure**: geometry, fancyhdr, titlesec, parskip

**Mathematics**: amsmath, amssymb, mathtools, amsthm

**Graphics**: graphicx, tikz, pgfplots, subcaption, float

**Tables**: booktabs, longtable, multirow

**References**: biblatex, hyperref, cleveref

**Typography**: fontenc, microtype, xcolor

**Code**: listings, minted

## Key Files

| File | Purpose |
|------|---------|
| `src/main.tex` | Main document entry point |
| `src/preamble/packages.tex` | All package imports |
| `src/preamble/settings.tex` | Document configuration |
| `src/preamble/commands.tex` | Custom commands/macros |
| `Makefile` | Build commands |
| `.latexmkrc` | LaTeX build configuration |
| `.github/workflows/build.yml` | CI/CD workflow |

## Scripts (Python/uv)

All scripts use uv inline dependencies (PEP 723) and run operations in Docker:

| Script | Purpose |
|--------|---------|
| `scripts/setup.py` | Check Docker, pull image |
| `scripts/init.py` | Interactive project customization wizard |
| `scripts/build.py` | Compile documents (Docker) |
| `scripts/clean.py` | Remove build artifacts |
| `scripts/test.py` | Run tests (Docker) |
| `scripts/lint.py` | Run linter (Docker) |
| `scripts/watch.py` | Auto-rebuild (Docker) |

## Build Configuration

- **Docker Image**: `texlive/texlive:latest-full`
- **LaTeX Engine**: pdflatex (configurable in `.latexmkrc`)
- **Document Class**: article
- **Bibliography**: BibLaTeX with biber backend
- **Shell Escape**: Enabled for minted

## Requirements

- **Docker** - Required for all builds (no local LaTeX needed!)
- **Python 3.12+** - For build scripts
- **uv** - Python package manager

Optional:
- **act** - For local GitHub Actions testing
- **TeX Live** - Only if you want to use `make build-local`

## Adding Content

1. **New chapter**: Create `src/chapters/NN-name.tex`, include in `main.tex`
2. **New image**: Place in `src/assets/images/`, use `\includegraphics`
3. **New citation**: Add to `src/bibliography/references.bib`, use `\cite`
4. **New package**: Add to `src/preamble/packages.tex`

## Documentation

See `docs/` for detailed guides:
- `01-getting-started.md` - Quick start
- `02-project-structure.md` - Directory layout
- `03-latex-packages.md` - Package usage
- `04-building.md` - Build instructions
- `05-testing.md` - Testing guide
- `06-customization.md` - How to extend

## CI/CD

GitHub Actions automatically builds on:
- Push to main/master
- Pull requests
- Manual dispatch

Test locally with: `make test` (requires Docker and act)

## CLAUDE.md Files

Each directory contains a CLAUDE.md explaining:
- Directory purpose
- File conventions
- How to add/modify content

## Keeping This File Updated

This CLAUDE.md is the primary reference for AI assistants and developers. Keep it in sync with:

| Change | Update Here |
|--------|-------------|
| New make target | Quick Commands section |
| New script in `scripts/` | Scripts table |
| New directory | Directory Structure |
| New package added | Included Packages |
| Changed requirements | Requirements section |
| New doc file | Documentation section |

**Priority**: This file should be updated alongside any structural changes to the project.

## Development Guidelines

When making changes to this repository:

1. **Update documentation**: Any changes to features, workflows, or configuration MUST be reflected in the relevant documentation files in `docs/`.
2. **Update CLAUDE.md files**: If directory structure or conventions change, update the relevant CLAUDE.md file.
3. **Test changes**: Run `make test` before committing.
4. **Keep README.md in sync**: Major feature changes should be reflected in README.md.

---

*See README.md for user-facing documentation.*
