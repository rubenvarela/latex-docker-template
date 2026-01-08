# assets/ - Document Assets

This directory contains external resources used in the document.

## Purpose

Store images, figures, and other non-LaTeX assets in an organized manner.

## Structure

```
assets/
├── images/     # Raster images (PNG, JPG, PDF)
├── figures/    # TikZ/vector graphics source files
└── CLAUDE.md
```

## Subdirectories

### images/

For raster images and pre-rendered graphics:
- PNG files (screenshots, photos)
- JPG files (photographs)
- PDF files (vector graphics, diagrams from other tools)

### figures/

For TikZ/PGF source files:
- `.tex` files with standalone TikZ code
- Reusable diagram templates

## Graphics Path

The graphics path is configured in `src/preamble/settings.tex`:

```latex
\graphicspath{
    {../assets/images/}
    {../assets/figures/}
}
```

This means you can include images without the full path:

```latex
\includegraphics{my-image}  % Finds assets/images/my-image.png
```

## Including Assets

### Simple Image

```latex
\includegraphics[width=0.8\textwidth]{image-name}
```

### Figure with Caption

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{image-name}
    \caption{Description of the image}
    \label{fig:image-label}
\end{figure}
```

### TikZ Figure

```latex
\begin{figure}[htbp]
    \centering
    \input{../assets/figures/diagram.tex}
    \caption{TikZ diagram}
    \label{fig:diagram}
\end{figure}
```

## File Naming

- **Lowercase**: `my-image.png` not `My-Image.PNG`
- **Hyphens**: `circuit-diagram.pdf` not `circuit_diagram.pdf`
- **Descriptive**: `results-comparison-chart.pdf`
- **No spaces**: Use hyphens instead

## Supported Formats

| Format | Best For |
|--------|----------|
| PNG | Screenshots, diagrams with transparency |
| JPG | Photographs |
| PDF | Vector graphics, plots from other tools |
| EPS | Legacy vector format (needs conversion) |

## Best Practices

1. **Use vector when possible**: PDF/TikZ for diagrams
2. **Reasonable resolution**: 150-300 DPI for print, 72-150 for screen
3. **Optimize file size**: Compress large images
4. **Consistent naming**: Use a clear naming scheme
5. **Version control**: Avoid committing huge binary files
