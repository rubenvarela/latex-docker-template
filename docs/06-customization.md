# Customization

This guide explains how to customize and extend the LaTeX template.

## Quick Customization

### Document Metadata

Edit `src/main.tex`:

```latex
\title{Your Document Title}
\author{Your Name}
\date{\today}  % or specific date
```

### Page Layout

Edit `src/preamble/packages.tex`:

```latex
\usepackage[
    margin=1in,           % Change margins
    top=1.5in,            % Different top margin
    headheight=14pt,
    letterpaper           % or a4paper
]{geometry}
```

### Header/Footer

Edit `src/preamble/settings.tex`:

```latex
\fancyhead[L]{Left Header}
\fancyhead[C]{Center Header}
\fancyhead[R]{Right Header}
\fancyfoot[C]{\thepage}
```

### Colors

Edit `src/preamble/packages.tex` or `styles/template.sty`:

```latex
\definecolor{myblue}{RGB}{0, 82, 147}
\definecolor{linkcolor}{HTML}{0066CC}
```

Update hyperref colors:

```latex
\hypersetup{
    linkcolor=myblue,
    citecolor=myblue,
    urlcolor=myblue
}
```

## Adding Content

### New Chapter

1. Create file: `src/chapters/01-new-chapter.tex`

```latex
\section{Chapter Title}
\label{sec:chapter-title}

Your content here.

\subsection{Subsection}

More content.
```

2. Include in `src/main.tex`:

```latex
\input{chapters/00-introduction}
\input{chapters/01-new-chapter}  % Add this line
```

### New Section in Existing Chapter

Just add to the chapter file:

```latex
\section{New Section}
\label{sec:new-section}

Content goes here.
```

### Images

1. Place image in `assets/images/`
2. Include in your document:

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{image-filename}
    \caption{Image caption}
    \label{fig:image-label}
\end{figure}
```

### Tables

```latex
\begin{table}[htbp]
    \centering
    \caption{Table caption}
    \label{tab:table-label}
    \begin{tabular}{lrr}
        \toprule
        Column 1 & Column 2 & Column 3 \\
        \midrule
        Data & 123 & 456 \\
        \bottomrule
    \end{tabular}
\end{table}
```

### Bibliography Entries

Add to `src/bibliography/references.bib`:

```bibtex
@article{smith2024,
    author = {Smith, John and Doe, Jane},
    title = {Article Title},
    journal = {Journal Name},
    year = {2024},
    volume = {10},
    pages = {1--20},
    doi = {10.1234/example}
}
```

Cite in document:

```latex
According to \cite{smith2024}, ...
```

## Custom Commands

Add to `src/preamble/commands.tex`:

### Math Shortcuts

```latex
% Number sets
\newcommand{\R}{\mathbb{R}}
\newcommand{\N}{\mathbb{N}}

% Operators
\DeclareMathOperator{\argmax}{arg\,max}

% Shortcuts
\newcommand{\norm}[1]{\left\|#1\right\|}
```

### Text Commands

```latex
\newcommand{\ie}{\textit{i.e.}}
\newcommand{\eg}{\textit{e.g.}}
\newcommand{\code}[1]{\texttt{#1}}
```

### Environments

```latex
\newenvironment{important}{%
    \begin{quote}
    \textbf{Important:}
}{%
    \end{quote}
}
```

## Custom Styles

### Create New Style File

1. Create `styles/custom.sty`:

```latex
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{custom}[2024/01/01 Custom Styles]

% Your customizations
\newcommand{\mycommand}{...}

\endinput
```

2. Include in `src/preamble/packages.tex`:

```latex
\usepackage{../styles/custom}
```

### Modify Template Style

Edit `styles/template.sty` for template-wide changes.

## Document Classes

### Changing Document Class

Edit `src/main.tex`:

```latex
% Article (default)
\documentclass[11pt, letterpaper]{article}

% Report (with chapters)
\documentclass[11pt, letterpaper]{report}

% Book
\documentclass[11pt, letterpaper]{book}
```

### Class-Specific Adjustments

For `report` or `book`, you may want chapters:

```latex
\chapter{Chapter Title}
\section{Section}
```

And adjust the chapter style in `src/preamble/settings.tex`.

## Build Customization

### Different Main File

Edit `Makefile`:

```makefile
MAIN_TEX := src/your-document.tex
```

### Different Output Directory

Edit `Makefile` and `.latexmkrc`:

```makefile
BUILD_DIR := output
```

```perl
$out_dir = 'output';
```

### Additional Make Targets

Add to `Makefile`:

```makefile
## my-target: Description of target
my-target:
    @echo "Running custom target..."
    @./scripts/my-script.py
```

## Adding Packages

1. Add to `src/preamble/packages.tex`:

```latex
\usepackage{newpackage}
```

2. Test with `make build-test`

3. Document if complex (in `docs/03-latex-packages.md`)

## CI/CD Customization

### Change Workflow Triggers

Edit `.github/workflows/build.yml`:

```yaml
on:
  push:
    branches: [main, develop]  # Add branches
  schedule:
    - cron: '0 0 * * 1'  # Weekly builds
```

### Add Build Steps

```yaml
steps:
  - name: Custom step
    run: ./scripts/custom-script.py
```

### Change Docker Image

```yaml
container:
  image: your-custom-image:tag
```

## Best Practices

1. **Keep changes modular**: Use separate files for major customizations
2. **Document changes**: Update CLAUDE.md files and docs
3. **Test thoroughly**: Run `make build-test` after package changes
4. **Version control**: Commit incrementally with clear messages
5. **Don't modify core files unnecessarily**: Prefer adding over changing
