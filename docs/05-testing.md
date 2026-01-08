# Testing

This guide explains how to test your LaTeX setup and CI/CD pipeline.

All tests run inside Docker - no local LaTeX installation required!

## Quick Reference

```bash
make test         # Run all tests (Docker)
make build-test   # Build test document (Docker)
make lint         # Run LaTeX linter (Docker)
make validate     # Validate syntax (Docker)
make act          # Run GitHub Actions with act (requires act)
```

## Running Tests

### Basic Test Suite

```bash
make test
```

This runs tests in Docker to verify:
- biber (bibliography processor) is available
- Pygments (for minted code highlighting) is available
- Test document compiles successfully
- chktex linting passes

### Test Options

```bash
# Run tests with verbose output
./scripts/test.py --verbose

# Skip compilation (faster, just check tools)
./scripts/test.py --skip-compile

# Test a specific document
./scripts/test.py --test-doc src/main.tex
```

## Test Document

The template includes a comprehensive test document that exercises all packages.

### Building the Test Document

```bash
make build-test
```

This compiles `tests/test_document.tex` which tests:
- All document structure packages
- All math packages with equations
- TikZ graphics and PGFPlots charts
- Tables with booktabs, longtable, multirow
- Code listings with both listings and minted
- Bibliography and cross-references
- Typography and color

### What Success Looks Like

If the test document compiles without errors, all packages are working correctly.

Check `build/test_document.pdf` for:
- ✅ All sections render properly
- ✅ Math equations display correctly
- ✅ TikZ diagrams appear
- ✅ Code has syntax highlighting
- ✅ Bibliography entries show
- ✅ Cross-references resolve

## Linting

### Run the Linter

```bash
make lint
```

Or with more options:

```bash
# Show all warnings
./scripts/lint.py --verbose

# Also run lacheck (additional linter)
./scripts/lint.py --lacheck

# Lint a specific file
./scripts/lint.py --file src/main.tex

# Fail on any warnings (for CI)
./scripts/lint.py --strict
```

### Common Warnings

- Missing `~` before `\cite` or `\ref`
- Interword spacing issues
- Parenthesis/bracket mismatches

## Validation

Quick syntax check without full compilation:

```bash
make validate
```

This catches syntax errors faster than a full build.

## GitHub Actions Testing

### Using act (Optional)

If you want to test the exact GitHub Actions workflow locally:

1. Install act:
   ```bash
   # macOS
   brew install act

   # Linux
   curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
   ```

2. Run the workflow:
   ```bash
   make act
   ```

### Troubleshooting act

#### First run is slow

The first run downloads Docker images (~4GB for texlive). Subsequent runs use cached images.

#### Architecture issues (Apple Silicon)

If you see architecture-related errors on M1/M2 Macs, edit `.actrc`:

```
--container-architecture linux/amd64
```

## CI/CD Pipeline

### Workflow Triggers

The GitHub Actions workflow runs on:

1. **Push to main**: Builds main document
2. **Pull requests**: Builds and validates changes
3. **Manual dispatch**: Can optionally build test document

### Workflow Jobs

| Job | Purpose | When |
|-----|---------|------|
| `build` | Compile main document, auto-release | Always |
| `build-test` | Compile test document | Main branch only |
| `release` | Create formal GitHub release | Version tags (v*) |

### Auto-Release on Every Build

Every successful build automatically uploads the PDF to GitHub Releases:

**Filename format**: `document-{branch}-{timestamp}.pdf`
- Example: `document-main-20260107-163045.pdf`

**Release strategy**:
| Branch | Behavior | Tag Format |
|--------|----------|------------|
| `main` | **Accumulate** - keeps all builds | `builds/main-{timestamp}` |
| Other branches | **Rolling** - replaces previous | `builds/{branch}` |

This allows tracking document iterations without manual tagging.

### Artifacts

Build artifacts are uploaded (GitHub Actions only, not in local `act` testing):
- `document-{branch}-{timestamp}`: The compiled PDF
- `test-document`: Test document PDF (main branch only)
- `build-logs`: Logs on failure

Retention: 30 days (configurable in workflow).

> **Note**: When running locally with `act`, release upload and artifact upload are skipped (detected via `ACT=true` environment variable).

### Creating Formal Releases

For versioned releases, tag with a version:

```bash
git tag v1.0.0
git push origin v1.0.0
```

The workflow will:
1. Build the document
2. Create a formal GitHub release
3. Attach the PDF as `document-v1.0.0.pdf`

## Test Checklist

Before committing changes:

- [ ] `make test` passes
- [ ] `make build` succeeds
- [ ] `make build-test` succeeds (if changing packages)
- [ ] `make lint` has no critical warnings
- [ ] PDF looks correct

## Continuous Integration Best Practices

1. **Always test locally first**: Use `make test` before pushing
2. **Use draft mode for iteration**: `make build-draft` is faster
3. **Check test document after package changes**: `make build-test`
4. **Keep PRs focused**: Easier to debug build failures
5. **Review workflow logs**: Check GitHub Actions output on failure
