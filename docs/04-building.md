# Building Documents

This guide explains how to build LaTeX documents using the template.

All builds run inside Docker by default - no local LaTeX installation required!

## Quick Reference

```bash
make build        # Full build (Docker)
make build-draft  # Quick draft build (Docker)
make build-test   # Build test document (Docker)
make watch        # Auto-rebuild on changes (Docker)
make clean        # Remove artifacts
make build-local  # Build with local LaTeX (no Docker)
```

## Build Methods

### Method 1: Make Commands (Recommended)

The Makefile provides convenient commands that run builds in Docker:

```bash
# Full build with bibliography
make build

# Quick draft (single pass, no bibliography)
make build-draft

# Watch mode - auto-rebuild on file changes
make watch
```

### Method 2: Direct Script Execution

Run Python scripts directly:

```bash
./scripts/build.py --src src/main.tex --output build
./scripts/build.py --src src/main.tex --draft
./scripts/build.py --src src/main.tex --local  # Use local LaTeX
```

### Method 3: Docker Shell

For debugging or manual commands, open a shell in the container:

```bash
make docker-shell

# Inside the container:
latexmk -pdf -shell-escape src/main.tex
```

### Method 4: Local Build (requires local LaTeX)

If you have TeX Live installed locally:

```bash
make build-local

# Or directly:
cd src && latexmk -pdf main.tex
```

## Build Modes

### Full Build

Runs multiple passes for:
- Cross-references resolution
- Bibliography processing (biber)
- Table of contents generation

```bash
make build
```

Time: ~10-30 seconds depending on document size.

### Draft Build

Single pass, skips bibliography:
- Faster iteration during writing
- May have unresolved references

```bash
make build-draft
```

Time: ~3-5 seconds.

### Watch Mode

Monitors files and auto-rebuilds:

```bash
make watch
```

Features:
- Watches `src/`, `styles/`, `assets/`
- Debounces rapid changes (1 second)
- Shows build status in terminal

Stop with `Ctrl+C`.

## Build Output

All output goes to `build/`:

```
build/
├── main.pdf          # The compiled document
├── main.log          # Build log (check for warnings)
├── main.aux          # Auxiliary data
├── main.bbl          # Bibliography data
├── main.toc          # Table of contents data
└── ...
```

## Build Configuration

### latexmkrc

The `.latexmkrc` file configures the build:

```perl
# Use pdflatex
$pdf_mode = 1;
$pdflatex = 'pdflatex -shell-escape -interaction=nonstopmode %O %S';

# Output directory
$out_dir = 'build';

# Use biber for bibliography
$biber = 'biber %O %S';
```

### Changing LaTeX Engine

Edit `.latexmkrc` to use LuaLaTeX or XeLaTeX:

```perl
# For LuaLaTeX
$pdf_mode = 4;
$lualatex = 'lualatex -shell-escape %O %S';

# For XeLaTeX
$pdf_mode = 5;
$xelatex = 'xelatex -shell-escape %O %S';
```

## Troubleshooting

### Build Fails

1. Check the log file:
   ```bash
   cat build/main.log | grep -i error
   ```

2. Look for missing packages:
   ```
   ! LaTeX Error: File `package.sty' not found.
   ```

3. Run `make clean` and rebuild:
   ```bash
   make clean && make build
   ```

### Minted Errors

Minted requires shell-escape and Pygments:

1. Verify Pygments is installed:
   ```bash
   python3 -c "import pygments; print(pygments.__version__)"
   ```

2. Install if missing:
   ```bash
   pip install Pygments
   ```

3. Ensure shell-escape is enabled (it is in `.latexmkrc`).

### Bibliography Not Appearing

1. Ensure `.bib` file has entries
2. Ensure entries are cited in the document
3. Run full build (not draft):
   ```bash
   make clean && make build
   ```

4. Check for biber errors:
   ```bash
   cat build/main.blg
   ```

### Undefined References

Run the build again - may need multiple passes:

```bash
make build
```

Or clean and rebuild:

```bash
make clean && make build
```

### Build Too Slow

1. Use draft mode for iterations:
   ```bash
   make build-draft
   ```

2. Use watch mode to only rebuild changed files:
   ```bash
   make watch
   ```

3. Consider TikZ externalization for complex graphics.

## CI/CD Builds

GitHub Actions automatically builds on:
- Push to main
- Pull requests
- Manual trigger

See `.github/workflows/build.yml` for configuration.

### Local CI Testing

Test locally before pushing:

```bash
make test      # Run tests in Docker (biber, Pygments, compilation)
make act-test  # Test GitHub Actions build job (requires act)
```
