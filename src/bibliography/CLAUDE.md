# src/bibliography/ - Bibliography Files

This directory contains BibLaTeX bibliography database files.

## Purpose

Store bibliography entries for citations in the document.

## Files

| File | Purpose |
|------|---------|
| `references.bib` | Main bibliography database |

## BibLaTeX Format

Entries follow standard BibLaTeX format:

```bibtex
@article{author2024keyword,
    author = {Last, First and Other, Author},
    title = {Article Title},
    journal = {Journal Name},
    year = {2024},
    volume = {10},
    number = {2},
    pages = {1--20},
    doi = {10.1234/example}
}

@book{author2024book,
    author = {Last, First},
    title = {Book Title},
    publisher = {Publisher Name},
    year = {2024},
    isbn = {978-0-000-00000-0}
}

@inproceedings{author2024conf,
    author = {Last, First},
    title = {Conference Paper Title},
    booktitle = {Conference Name},
    year = {2024},
    pages = {1--10}
}

@online{website2024,
    author = {{Organization Name}},
    title = {Page Title},
    year = {2024},
    url = {https://example.com},
    urldate = {2024-01-15}
}
```

## Citation Key Convention

Use format: `authorYYYYkeyword`
- `author`: First author's last name (lowercase)
- `YYYY`: Publication year
- `keyword`: Short descriptive word

Examples:
- `smith2024neural`
- `johnson2023climate`
- `team2024report`

## Citing in Documents

```latex
\cite{smith2024neural}           % [1]
\textcite{smith2024neural}       % Smith (2024)
\parencite{smith2024neural}      % (Smith, 2024)
\cite{smith2024,johnson2023}     % [1, 2]
```

## Adding Entries

1. Open `references.bib`
2. Add entry in appropriate format
3. Use consistent citation key format
4. Rebuild document: `make build`

## Bibliography Tools

Recommended tools for managing entries:
- **Zotero**: Free, open-source reference manager
- **Mendeley**: Reference manager with cloud sync
- **JabRef**: BibTeX-focused manager
- **DOI lookup**: Many tools can auto-generate from DOI

## Multiple Bibliography Files

To add additional `.bib` files:

1. Create new file: `additional.bib`
2. Add to `src/preamble/settings.tex`:
   ```latex
   \addbibresource{bibliography/references.bib}
   \addbibresource{bibliography/additional.bib}
   ```

## Common Issues

- **Entry not appearing**: Ensure it's cited in the document
- **Formatting issues**: Check for missing commas or braces
- **Biber errors**: Check `build/main.blg` for details
