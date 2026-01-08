# Getting Started

This guide will help you set up and start using the LaTeX template repository.

## Prerequisites

All builds run inside Docker - no local LaTeX installation required!

### Required

1. **Docker**
   - macOS/Windows: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Linux: [Docker Engine](https://docs.docker.com/engine/install/)
   - Check: `docker --version`

2. **Python 3.12+**
   - Check: `python3 --version`

3. **uv** (Python package manager)
   - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Check: `uv --version`

### Optional

4. **act** (GitHub Actions local runner)
   - macOS: `brew install act`
   - [Other platforms](https://github.com/nektos/act#installation)

5. **TeX Live** (only for `make build-local`)
   - macOS: `brew install --cask mactex`
   - Ubuntu: `sudo apt install texlive-full`

## Quick Start

### 1. Clone or Use as Template

```bash
# Option A: Clone directly
git clone <repository-url> my-document
cd my-document

# Option B: Use GitHub's "Use this template" button
# Then clone your new repository
```

### 2. Verify Your Environment

```bash
make setup
```

This checks that Docker is available and pulls the LaTeX image.

### 3. Initialize Your Project

```bash
make init
```

This interactive wizard will:
- Set your document title and author
- Update PDF metadata
- Optionally clear sample content
- Optionally reset git history for a fresh start

### 4. Build the Document

```bash
make build
```

The compiled PDF will be in `build/main.pdf`.

### 5. View the PDF

```bash
# macOS
make open

# Or manually open build/main.pdf
```

## Next Steps

After running `make init`:
- Add content to `src/chapters/00-introduction.tex`
- Create new chapters in `src/chapters/`
- Add images to `src/assets/images/`
- Update bibliography in `src/bibliography/references.bib`
- Use `make watch` for auto-rebuild while editing

## Common Tasks

### Add a New Chapter

1. Create a new file: `src/chapters/01-my-chapter.tex`
2. Add content to the file
3. Include it in `src/main.tex`:
   ```latex
   \input{chapters/01-my-chapter}
   ```

### Add an Image

1. Place the image in `src/assets/images/`
2. Include in your document:
   ```latex
   \includegraphics[width=0.8\textwidth]{my-image.png}
   ```

### Add a Citation

1. Add entry to `src/bibliography/references.bib`
2. Cite in your document: `\cite{citation-key}`
3. Bibliography is automatically printed at the end

## Troubleshooting

### Docker not running

```
Error: Docker daemon is not running
```

Start Docker Desktop or the Docker daemon before running builds.

### First build is slow

The first `make setup` downloads the TeX Live Docker image (~4GB).
Subsequent builds are much faster as the image is cached.

### Build takes too long

Use draft mode for quick iterations:
```bash
make build-draft
```

### Want to use local LaTeX?

If you have TeX Live installed locally and prefer not to use Docker:
```bash
make build-local
```

## Getting Help

- Check the [documentation](./02-project-structure.md) for detailed information
- Review the test document in `tests/test_document.tex` for examples
- Open an issue on GitHub for bugs or questions
