# LaTeX Packages

This document describes all LaTeX packages included in the template and how to use them.

## Package Categories

The template includes packages organized into these categories:
1. Document Structure & Formatting
2. Mathematics
3. Graphics & Figures
4. Tables
5. References & Citations
6. Typography & Fonts
7. Code Listings

## Document Structure & Formatting

### geometry

Customizes page layout and margins.

```latex
\usepackage[margin=1in, headheight=14pt]{geometry}
```

**Configuration**: Edit `src/preamble/packages.tex` to change margins.

### fancyhdr

Creates custom headers and footers.

```latex
\pagestyle{fancy}
\fancyhead[L]{Left header}
\fancyhead[R]{Right header}
\fancyfoot[C]{\thepage}
```

**Configuration**: Edit `src/preamble/settings.tex` for header/footer setup.

### titlesec

Customizes section titles and headings.

```latex
\titleformat{\section}
    {\normalfont\Large\bfseries}
    {\thesection}
    {1em}
    {}
```

### parskip

Adjusts paragraph spacing (space between paragraphs instead of indent).

Loaded automatically - no configuration needed.

## Mathematics

### amsmath

Essential mathematical typesetting.

```latex
% Inline math
$E = mc^2$

% Display equation
\begin{equation}
    \int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
\end{equation}

% Aligned equations
\begin{align}
    f(x) &= x^2 + 2x + 1 \\
    &= (x + 1)^2
\end{align}
```

### amssymb

Additional mathematical symbols.

```latex
% Number sets
\mathbb{R}, \mathbb{N}, \mathbb{Z}, \mathbb{Q}, \mathbb{C}

% Arrows
\Rightarrow, \Leftrightarrow, \to

% Relations
\leq, \geq, \neq, \approx
```

### mathtools

Extended amsmath features.

```latex
% Automatic delimiter sizing
\left( \frac{a}{b} \right)

% Matrices
\begin{pmatrix} a & b \\ c & d \end{pmatrix}
\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}
```

### amsthm

Theorem environments.

```latex
\begin{theorem}
    Statement of the theorem.
\end{theorem}

\begin{proof}
    Proof of the theorem.
\end{proof}

\begin{lemma}
    Supporting lemma.
\end{lemma}

\begin{definition}
    Definition of a term.
\end{definition}
```

**Custom environments**: Defined in `src/preamble/commands.tex`.

## Graphics & Figures

### graphicx

Includes and manipulates images.

```latex
\includegraphics[width=0.8\textwidth]{image-name}

% Options
\includegraphics[width=5cm, angle=45]{image}
\includegraphics[scale=0.5]{image}
```

**Graphics path**: Set in `src/preamble/settings.tex`.

### tikz

Creates vector graphics programmatically.

```latex
\begin{tikzpicture}
    \draw (0,0) -- (2,0) -- (2,2) -- cycle;
    \fill[blue] (1,1) circle (0.5);
    \node at (1,1) {Text};
\end{tikzpicture}
```

**Libraries loaded**: arrows.meta, positioning, shapes, calc, backgrounds

### pgfplots

Creates scientific plots and charts.

```latex
\begin{tikzpicture}
    \begin{axis}[
        xlabel={$x$},
        ylabel={$f(x)$},
    ]
        \addplot[blue, thick] {x^2};
    \end{axis}
\end{tikzpicture}
```

### subcaption

Manages subfigures.

```latex
\begin{figure}
    \begin{subfigure}[b]{0.45\textwidth}
        \includegraphics{image1}
        \caption{First image}
    \end{subfigure}
    \begin{subfigure}[b]{0.45\textwidth}
        \includegraphics{image2}
        \caption{Second image}
    \end{subfigure}
    \caption{Overall caption}
\end{figure}
```

### float

Improved float placement control.

```latex
\begin{figure}[H]  % H = "here" - don't float
    ...
\end{figure}
```

## Tables

### booktabs

Professional table formatting.

```latex
\begin{tabular}{lrr}
    \toprule
    Header 1 & Header 2 & Header 3 \\
    \midrule
    Data 1 & Data 2 & Data 3 \\
    Data 4 & Data 5 & Data 6 \\
    \bottomrule
\end{tabular}
```

### longtable

Tables spanning multiple pages.

```latex
\begin{longtable}{ll}
    \caption{Long table} \\
    \toprule
    Header 1 & Header 2 \\
    \midrule
    \endfirsthead
    ...
\end{longtable}
```

### multirow

Cells spanning multiple rows.

```latex
\multirow{2}{*}{Spanning cell} & Row 1 \\
                               & Row 2 \\
```

## References & Citations

### biblatex

Modern bibliography management.

```latex
% In preamble (already configured)
\addbibresource{bibliography/references.bib}

% In document
\cite{key}           % Basic citation
\textcite{key}       % "Author (year)"
\parencite{key}      % "(Author, year)"

% Print bibliography
\printbibliography
```

**Bibliography file**: `src/bibliography/references.bib`

### hyperref

Clickable links and PDF bookmarks.

```latex
\url{https://example.com}
\href{https://example.com}{Link text}
\href{mailto:email@example.com}{email}
```

**Configuration**: Set in `src/preamble/packages.tex`.

### cleveref

Intelligent cross-referencing.

```latex
\label{sec:intro}
\label{eq:main}
\label{fig:diagram}

\cref{sec:intro}     % "Section 1"
\Cref{sec:intro}     % "Section 1" (capitalized)
\cref{eq:main}       % "Equation 1"
\cref{fig:diagram}   % "Figure 1"
```

## Typography & Fonts

### fontenc

Proper font encoding.

```latex
\usepackage[T1]{fontenc}
```

Enables proper hyphenation and special characters.

### microtype

Micro-typography improvements.

Loaded automatically - improves letterspacing and margin kerning.

### xcolor

Color support.

```latex
\textcolor{red}{Red text}
\colorbox{yellow}{Highlighted}

% Custom colors
\definecolor{mycolor}{RGB}{100, 150, 200}
\textcolor{mycolor}{Custom color}
```

**Custom colors**: Define in `src/preamble/packages.tex` or `styles/template.sty`.

## Code Listings

### listings

Basic code formatting.

```latex
\begin{lstlisting}[language=Python]
def hello():
    print("Hello, World!")
\end{lstlisting}
```

**Configuration**: Default style in `src/preamble/packages.tex`.

### minted

Syntax highlighting with Pygments.

```latex
\begin{minted}{python}
def hello():
    print("Hello, World!")
\end{minted}

% Inline code
\mintinline{python}{print("Hello")}
```

**Requirements**:
- Python with Pygments installed
- Compile with `-shell-escape` (configured in `.latexmkrc`)

## Adding New Packages

1. Add the package to `src/preamble/packages.tex`
2. Test by running `make build-test`
3. Document usage if non-trivial
