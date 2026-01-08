# tests/ - Test Documents

This directory contains test documents for verifying the template.

## Purpose

Provide comprehensive tests to verify all LaTeX packages work correctly.

## Files

| File | Purpose |
|------|---------|
| `test_document.tex` | Comprehensive test exercising all packages |
| `fixtures/` | Test assets (images, data) |

## test_document.tex

A comprehensive document that tests:

### Document Structure
- geometry (margins)
- fancyhdr (headers/footers)
- titlesec (section formatting)
- parskip (paragraph spacing)

### Mathematics
- amsmath (equations, align)
- amssymb (symbols)
- mathtools (matrices)
- amsthm (theorems)

### Graphics
- graphicx (images)
- tikz (diagrams)
- pgfplots (charts)
- subcaption (subfigures)
- float (placement)

### Tables
- booktabs (professional tables)
- longtable (multi-page)
- multirow (spanning cells)

### Code
- listings (basic code)
- minted (syntax highlighting)

### References
- biblatex (citations)
- hyperref (links)
- cleveref (cross-refs)

### Typography
- fontenc (encoding)
- microtype (improvements)
- xcolor (colors)

## Running Tests

```bash
# Build test document
make build-test

# Build in Docker
make docker-test

# Run CI locally
make test
```

## Success Criteria

The test passes if:
1. Document compiles without errors
2. PDF is generated in `build/test_document.pdf`
3. All sections render correctly
4. No undefined references

## fixtures/

Test assets used by test_document.tex:
- Sample images for graphicx testing
- Test data files

## Adding Tests

To add new package tests:

1. Add package to test_document.tex preamble
2. Add a section demonstrating the package
3. Verify compilation: `make build-test`
4. Check the PDF for correct rendering

## Troubleshooting

If test fails:
1. Check `build/test_document.log` for errors
2. Look for missing packages
3. Verify minted has Pygments installed
4. Run `make clean` and retry
