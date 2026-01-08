# scripts/ - Build Automation Scripts

This directory contains Python scripts for build automation.

## Purpose

Provide automation for building, testing, and maintaining LaTeX documents.

**All builds run inside Docker by default** - users don't need local LaTeX installed.

## Scripts

| Script | Purpose | Make Target |
|--------|---------|-------------|
| `setup.py` | Check Docker, pull TeX Live image | `make setup` |
| `build.py` | Compile LaTeX documents (Docker) | `make build` |
| `clean.py` | Remove build artifacts | `make clean` |
| `test.py` | Run tests in Docker | `make test` |
| `lint.py` | Run LaTeX linter in Docker | `make lint` |
| `watch.py` | Auto-rebuild on file changes (Docker) | `make watch` |

## Docker Configuration

Scripts use `texlive/texlive:latest-full` Docker image by default.

All build scripts support `--local` flag to use local LaTeX instead:
```bash
./scripts/build.py --src src/main.tex --local
./scripts/watch.py --src src --local
```

## Script Format

All scripts use uv's inline script metadata (PEP 723):

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "click>=8.0.0",
#   "rich>=13.0.0",
# ]
# ///

"""Script description."""

import click
from rich.console import Console

@click.command()
def main():
    """Main function."""
    pass

if __name__ == "__main__":
    main()
```

## Running Scripts

### Via Make (recommended)

```bash
make setup
make build
make clean
make test
make watch
```

### Directly

```bash
./scripts/setup.py
./scripts/build.py --src src/main.tex --output build
./scripts/clean.py --dry-run
./scripts/test.py --verbose
./scripts/watch.py --src src
```

## Common Dependencies

| Package | Purpose |
|---------|---------|
| `click` | CLI argument parsing |
| `rich` | Beautiful terminal output |
| `watchdog` | File system monitoring |

## Adding a New Script

1. Create file: `scripts/newscript.py`

2. Add shebang and metadata:
```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["click>=8.0.0", "rich>=13.0.0"]
# ///
```

3. Make executable:
```bash
chmod +x scripts/newscript.py
```

4. Add Make target in `Makefile`:
```makefile
## new-target: Description
new-target:
    @./scripts/newscript.py
```

## Script Guidelines

- **Self-contained**: All dependencies in script header
- **CLI interface**: Use click for arguments
- **Rich output**: Use rich for formatted output
- **Error handling**: Return appropriate exit codes
- **Documentation**: Include docstrings and help text

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Argument error |
| 130 | Interrupted (Ctrl+C) |
