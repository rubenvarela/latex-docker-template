#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "rich>=13.0.0",
# ]
# ///
"""
Project initialization script for LaTeX Template Repository.

Interactive wizard that customizes the template for a new project.

Usage:
    ./scripts/init.py
    make init
"""

import shutil
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()

# Project root (parent of scripts directory)
PROJECT_ROOT = Path(__file__).parent.parent


def update_file(filepath: Path, replacements: dict[str, str]) -> bool:
    """Update a file with string replacements."""
    try:
        content = filepath.read_text()
        for old, new in replacements.items():
            content = content.replace(old, new)
        filepath.write_text(content)
        return True
    except Exception as e:
        console.print(f"[red]Error updating {filepath}: {e}[/red]")
        return False


def update_main_tex(title: str, author: str) -> bool:
    """Update src/main.tex with title and author."""
    filepath = PROJECT_ROOT / "src" / "main.tex"
    return update_file(filepath, {
        "\\title{Document Title}": f"\\title{{{title}}}",
        "\\author{Author Name}": f"\\author{{{author}}}",
    })


def update_packages_tex(title: str, author: str) -> bool:
    """Update src/preamble/packages.tex with PDF metadata."""
    filepath = PROJECT_ROOT / "src" / "preamble" / "packages.tex"
    return update_file(filepath, {
        "pdftitle={Document Title}": f"pdftitle={{{title}}}",
        "pdfauthor={Author Name}": f"pdfauthor={{{author}}}",
        "pdfsubject={Subject}": f"pdfsubject={{{title}}}",
    })


def clear_introduction() -> bool:
    """Clear the sample introduction content."""
    filepath = PROJECT_ROOT / "src" / "chapters" / "00-introduction.tex"
    try:
        content = """% =============================================================================
% Introduction
% =============================================================================

\\section{Introduction}

% Your content here.

"""
        filepath.write_text(content)
        return True
    except Exception as e:
        console.print(f"[red]Error clearing introduction: {e}[/red]")
        return False


def clear_bibliography() -> bool:
    """Clear the sample bibliography entries."""
    filepath = PROJECT_ROOT / "src" / "bibliography" / "references.bib"
    try:
        content = """% =============================================================================
% Bibliography - BibLaTeX References
% =============================================================================
% Add your references here.
% Use: \\cite{key} or \\textcite{key} in your document.
% =============================================================================

"""
        filepath.write_text(content)
        return True
    except Exception as e:
        console.print(f"[red]Error clearing bibliography: {e}[/red]")
        return False


def reset_git() -> bool:
    """Reset git history for a fresh start."""
    git_dir = PROJECT_ROOT / ".git"
    try:
        if git_dir.exists():
            shutil.rmtree(git_dir)
        subprocess.run(
            ["git", "init"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=True
        )
        return True
    except Exception as e:
        console.print(f"[red]Error resetting git: {e}[/red]")
        return False


def main():
    """Run the interactive initialization wizard."""
    console.print()
    console.print(Panel.fit(
        "[bold blue]LaTeX Template - Project Setup[/bold blue]\n\n"
        "Let's customize this template for your new document.",
        border_style="blue"
    ))
    console.print()

    # Gather information
    title = Prompt.ask(
        "[bold]Document title[/bold]",
        default="My Document"
    )

    author = Prompt.ask(
        "[bold]Author name[/bold]",
        default="Author Name"
    )

    console.print()

    delete_samples = Confirm.ask(
        "[bold]Delete sample content?[/bold] (introduction chapter)",
        default=True
    )

    delete_bib = Confirm.ask(
        "[bold]Delete sample bibliography?[/bold]",
        default=True
    )

    reset_git_history = Confirm.ask(
        "[bold]Reset git history?[/bold] (start fresh)",
        default=True
    )

    # Show summary
    console.print()
    table = Table(title="Summary", show_header=False, border_style="blue")
    table.add_column("Setting", style="bold")
    table.add_column("Value")
    table.add_row("Title", title)
    table.add_row("Author", author)
    table.add_row("Delete samples", "Yes" if delete_samples else "No")
    table.add_row("Delete bibliography", "Yes" if delete_bib else "No")
    table.add_row("Reset git", "Yes" if reset_git_history else "No")
    console.print(table)
    console.print()

    if not Confirm.ask("[bold]Proceed with these settings?[/bold]", default=True):
        console.print("[yellow]Cancelled.[/yellow]")
        return 0

    console.print()

    # Apply changes
    success = True

    console.print("Updating src/main.tex...", end=" ")
    if update_main_tex(title, author):
        console.print("[green]✓[/green]")
    else:
        success = False

    console.print("Updating src/preamble/packages.tex...", end=" ")
    if update_packages_tex(title, author):
        console.print("[green]✓[/green]")
    else:
        success = False

    if delete_samples:
        console.print("Clearing sample introduction...", end=" ")
        if clear_introduction():
            console.print("[green]✓[/green]")
        else:
            success = False

    if delete_bib:
        console.print("Clearing sample bibliography...", end=" ")
        if clear_bibliography():
            console.print("[green]✓[/green]")
        else:
            success = False

    if reset_git_history:
        console.print("Resetting git history...", end=" ")
        if reset_git():
            console.print("[green]✓[/green]")
        else:
            success = False

    console.print()

    if success:
        console.print(Panel.fit(
            "[bold green]✓ Project initialized![/bold green]\n\n"
            "Next steps:\n"
            "  1. Run [bold]make build[/bold] to compile\n"
            "  2. Edit [bold]src/chapters/[/bold] to add content\n"
            "  3. Run [bold]make watch[/bold] for auto-rebuild",
            border_style="green"
        ))
        return 0
    else:
        console.print("[red]Some operations failed. Check errors above.[/red]")
        return 1


if __name__ == "__main__":
    sys.exit(main())
