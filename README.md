# LaTeX Template Repository

A comprehensive template for building LaTeX documents with modern tooling, CI/CD automation, and best practices.

## Features

- **Docker-First Builds**: No local LaTeX installation required - just Docker!
- **Modular Structure**: Organized source files with separate preamble, chapters, and bibliography
- **All Essential Packages**: Pre-configured with 25+ commonly used LaTeX packages
- **Build Automation**: Makefile with setup, build, test, and clean targets
- **CI/CD Pipeline**: GitHub Actions workflow with auto-release on every build
- **Python Scripts**: uv-powered scripts for build automation

## Quick Start

```bash
# 1. Clone or use as template
git clone <repository-url>
cd latex-template

# 2. Verify your environment
make setup

# 3. Initialize your project (set title, author, etc.)
make init

# 4. Build the document
make build

# 5. Open the PDF (macOS)
make open
```

## Requirements

- **Docker**: All builds run in Docker - no local LaTeX installation needed!
- **Python 3.12+**: For build scripts
- **uv**: Python package manager ([install](https://astral.sh/uv))

Optional:
- **act**: For local GitHub Actions testing
- **TeX Live**: Only if you want to use `make build-local`

## Make Commands

| Command | Description |
|---------|-------------|
| `make setup` | Check Docker and pull the LaTeX image (~4GB) |
| `make init` | Interactive wizard to customize template (title, author) |
| `make build` | Compile the main document (Docker) |
| `make test` | Run tests to verify setup works (Docker) |
| `make clean` | Remove build artifacts |
| `make watch` | Watch for changes and auto-rebuild (Docker) |
| `make build-test` | Build the test document (Docker) |
| `make lint` | Run LaTeX linter (Docker) |
| `make docker-shell` | Open a shell in the container |
| `make build-local` | Build with local LaTeX (no Docker) |
| `make act` | Run GitHub Actions locally (requires act) |
| `make act-test` | Test GitHub Actions build job (faster) |
| `make help` | Show all available commands |

## Project Structure

```
├── src/                    # LaTeX source files (all document content)
│   ├── main.tex           # Main document entry point
│   ├── preamble/          # Package imports and settings
│   ├── chapters/          # Document chapters
│   ├── bibliography/      # .bib files
│   └── assets/            # Images and figures
├── styles/                 # Custom .sty files
├── scripts/               # Python build scripts
├── tests/                 # Test documents
├── docs/                  # Documentation
├── build/                 # Output directory (gitignored)
├── .github/workflows/     # CI/CD workflows
├── Makefile              # Build automation
└── CLAUDE.md             # AI assistant instructions
```

## Included Packages

### Document Structure
- geometry, fancyhdr, titlesec, parskip

### Mathematics
- amsmath, amssymb, mathtools, amsthm

### Graphics
- graphicx, tikz, pgfplots, subcaption, float

### Tables
- booktabs, longtable, multirow

### References
- biblatex, hyperref, cleveref

### Typography
- fontenc, microtype, xcolor

### Code
- listings, minted

## Documentation

See the `docs/` directory for detailed documentation:

1. [Getting Started](docs/01-getting-started.md)
2. [Project Structure](docs/02-project-structure.md)
3. [LaTeX Packages](docs/03-latex-packages.md)
4. [Building](docs/04-building.md)
5. [Testing](docs/05-testing.md)
6. [Customization](docs/06-customization.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `make build-test` to verify packages work
5. Submit a pull request

## License

MIT License - feel free to use this template for any project.
