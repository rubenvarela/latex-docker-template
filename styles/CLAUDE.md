# styles/ - Custom LaTeX Styles

This directory contains custom LaTeX style files (.sty).

## Purpose

Store reusable style definitions that can be shared across documents.

## Files

| File | Purpose |
|------|---------|
| `template.sty` | Main template style with colors and environments |

## template.sty

Contains:
- **Color palette**: Primary, secondary, accent colors
- **Custom environments**: Highlight boxes, warning boxes
- **Utility commands**: Horizontal rules, spacing shortcuts
- **PDF enhancements**: Hyperref color overrides

## Using Style Files

In your document preamble:

```latex
\usepackage{../styles/template}
```

Or copy to document directory and use:

```latex
\usepackage{template}
```

## Creating a New Style

1. Create file: `styles/mystyle.sty`

```latex
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{mystyle}[2024/01/01 My Custom Style]

% Package options
\DeclareOption{draft}{\def\mydraft{true}}
\ProcessOptions\relax

% Your definitions
\newcommand{\mycommand}{...}
\newenvironment{myenv}{...}{...}

\endinput
```

2. Include in document:

```latex
\usepackage{../styles/mystyle}
```

## Style File Structure

```latex
% Header
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{name}[date description]

% Required packages
\RequirePackage{xcolor}

% Options
\DeclareOption{option}{...}
\ProcessOptions\relax

% Definitions
% - Colors
% - Commands
% - Environments

% Footer
\endinput
```

## Best Practices

1. **Document everything**: Comment purpose of each definition
2. **Use options**: Make styles configurable
3. **Avoid conflicts**: Use unique names for commands
4. **Test thoroughly**: Verify with test document
5. **Version**: Include date in `\ProvidesPackage`

## Common Customizations

### Colors

```latex
\definecolor{myblue}{RGB}{0, 82, 147}
\definecolor{mygreen}{HTML}{28A745}
```

### Environments

```latex
\newenvironment{note}{%
    \par\medskip\noindent\textbf{Note:}
}{%
    \par\medskip
}
```

### Commands

```latex
\newcommand{\highlight}[1]{\colorbox{yellow}{#1}}
```
