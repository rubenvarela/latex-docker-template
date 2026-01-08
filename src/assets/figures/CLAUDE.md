# assets/figures/ - TikZ/Vector Figures

This directory stores TikZ source files for vector graphics.

## Purpose

Store reusable TikZ/PGF figure source files.

## File Format

Each figure should be a standalone `.tex` file:

```latex
% figure-name.tex
\begin{tikzpicture}
    % TikZ code here
    \draw (0,0) -- (2,2);
    \node at (1,1) {Label};
\end{tikzpicture}
```

## Usage

Include in your document:

```latex
\begin{figure}[htbp]
    \centering
    \input{../assets/figures/figure-name.tex}
    \caption{Figure caption}
    \label{fig:figure-name}
\end{figure}
```

Or inline:

```latex
\input{../assets/figures/simple-diagram.tex}
```

## Naming Convention

- Lowercase with hyphens
- Descriptive names
- `.tex` extension

Examples:
- `flowchart.tex`
- `network-diagram.tex`
- `data-pipeline.tex`

## TikZ Libraries

Common libraries are loaded in `src/preamble/packages.tex`:

```latex
\usetikzlibrary{
    arrows.meta,
    positioning,
    shapes,
    calc,
    backgrounds
}
```

To use additional libraries, add them to the preamble.

## Example Figure

```latex
% system-overview.tex
\begin{tikzpicture}[
    node distance=2cm,
    box/.style={
        rectangle,
        draw,
        minimum width=2.5cm,
        minimum height=1cm,
        align=center
    }
]
    \node[box] (input) {Input};
    \node[box, right of=input] (process) {Process};
    \node[box, right of=process] (output) {Output};

    \draw[-{Stealth}] (input) -- (process);
    \draw[-{Stealth}] (process) -- (output);
\end{tikzpicture}
```

## Best Practices

1. **Modular**: One figure per file
2. **Documented**: Comment complex parts
3. **Parameterized**: Use styles for consistency
4. **Tested**: Verify renders correctly before committing
