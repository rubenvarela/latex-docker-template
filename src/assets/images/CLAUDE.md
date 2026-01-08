# assets/images/ - Raster Images

This directory stores raster images for inclusion in documents.

## Purpose

Store PNG, JPG, and PDF images used in the document.

## Supported Formats

| Format | Use Case |
|--------|----------|
| PNG | Screenshots, diagrams, graphics with transparency |
| JPG | Photographs, images without transparency |
| PDF | Vector graphics exported from other tools |

## Usage

Include in your LaTeX document:

```latex
% Simple inclusion
\includegraphics{image-name}

% With width
\includegraphics[width=0.8\textwidth]{image-name}

% With figure environment
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.6\textwidth]{image-name}
    \caption{Image caption}
    \label{fig:image-name}
\end{figure}
```

Note: File extension is optional if unambiguous.

## Naming Convention

- Lowercase letters
- Hyphens for spaces
- Descriptive names
- No special characters

Examples:
- `results-graph.png`
- `system-architecture.pdf`
- `user-interface-screenshot.png`

## Image Guidelines

### Resolution

- **Print**: 300 DPI minimum
- **Screen/digital**: 150 DPI sufficient
- **Web export**: 72 DPI

### File Size

- Keep images under 1-2 MB when possible
- Compress large images before adding
- Consider PDF for vector content

### Transparency

- Use PNG for images needing transparency
- JPG does not support transparency

## Adding Images

1. Place image file in this directory
2. Use descriptive filename
3. Include in document with `\includegraphics`
4. Rebuild: `make build`
