#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "click>=8.0.0",
#   "rich>=13.0.0",
# ]
# ///
"""
LaTeX linter for LaTeX Template Repository.

Runs chktex inside Docker to check LaTeX files for common issues.
No local LaTeX installation required - just Docker.

Usage:
    ./scripts/lint.py
    ./scripts/lint.py --src src
    ./scripts/lint.py --fix  # Show suggestions
    make lint
"""

import subprocess
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

console = Console()

# Docker configuration
DOCKER_IMAGE = "texlive/texlive:latest-full"


def check_docker_available() -> bool:
    """Check if Docker is available and running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def find_tex_files(directory: Path, recursive: bool = True) -> list[Path]:
    """Find all .tex files in directory."""
    if recursive:
        return list(directory.rglob("*.tex"))
    return list(directory.glob("*.tex"))


def run_chktex(tex_file: Path, verbosity: int = 1) -> tuple[int, list[str]]:
    """
    Run chktex on a LaTeX file inside Docker.

    Args:
        tex_file: Path to .tex file
        verbosity: chktex verbosity level (0-3)

    Returns:
        Tuple of (warning_count, list of warnings)
    """
    cwd = Path.cwd()

    # Build chktex command
    # -v0 = quiet, -v1 = normal, -v2 = verbose, -v3 = very verbose
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{cwd}:/workspace",
        "-w", "/workspace",
        DOCKER_IMAGE,
        "chktex",
        f"-v{verbosity}",
        "-q",  # Quiet mode (no banner)
        str(tex_file)
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        # Parse output
        output = result.stdout + result.stderr
        warnings = [line.strip() for line in output.split('\n') if line.strip()]

        return len(warnings), warnings

    except subprocess.TimeoutExpired:
        return -1, ["Timeout running chktex"]
    except Exception as e:
        return -1, [f"Error: {e}"]


def run_lacheck(tex_file: Path) -> tuple[int, list[str]]:
    """
    Run lacheck on a LaTeX file inside Docker.

    Args:
        tex_file: Path to .tex file

    Returns:
        Tuple of (warning_count, list of warnings)
    """
    cwd = Path.cwd()

    cmd = [
        "docker", "run", "--rm",
        "-v", f"{cwd}:/workspace",
        "-w", "/workspace",
        DOCKER_IMAGE,
        "lacheck",
        str(tex_file)
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        output = result.stdout + result.stderr
        warnings = [line.strip() for line in output.split('\n') if line.strip()]

        return len(warnings), warnings

    except subprocess.TimeoutExpired:
        return -1, ["Timeout running lacheck"]
    except Exception as e:
        return -1, [f"Error: {e}"]


@click.command()
@click.option(
    '--src', '-s',
    default='src',
    type=click.Path(exists=True, path_type=Path),
    help='Directory containing .tex files to lint'
)
@click.option(
    '--file', '-f',
    type=click.Path(exists=True, path_type=Path),
    help='Specific .tex file to lint'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Show all warnings (not just summary)'
)
@click.option(
    '--lacheck', '-l',
    is_flag=True,
    help='Also run lacheck (additional linter)'
)
@click.option(
    '--strict', '-S',
    is_flag=True,
    help='Exit with error if any warnings found'
)
def main(src: Path, file: Path | None, verbose: bool, lacheck: bool, strict: bool):
    """
    Run LaTeX linters on source files.

    Uses chktex (and optionally lacheck) inside Docker to check for common
    LaTeX issues, style problems, and potential errors.

    All linting runs inside Docker - no local LaTeX installation required.
    """
    console.print(f"\n[bold blue]LaTeX Linter[/bold blue]")
    console.print(f"[dim]Docker image: {DOCKER_IMAGE}[/dim]\n")

    # Check Docker first
    if not check_docker_available():
        console.print("[red]✗ Docker is not available[/red]")
        console.print("Please start Docker and try again.")
        sys.exit(1)

    # Find files to lint
    if file:
        tex_files = [file]
    else:
        tex_files = find_tex_files(src)

    if not tex_files:
        console.print(f"[yellow]No .tex files found in {src}[/yellow]")
        sys.exit(0)

    console.print(f"[dim]Found {len(tex_files)} .tex file(s) to lint[/dim]\n")

    # Run linters
    total_warnings = 0
    file_results = []

    for tex_file in tex_files:
        console.print(f"[dim]Checking {tex_file}...[/dim]")

        # Run chktex
        count, warnings = run_chktex(tex_file)

        if count < 0:
            console.print(f"  [red]Error: {warnings[0]}[/red]")
            continue

        total_warnings += count

        # Optionally run lacheck
        lacheck_count = 0
        lacheck_warnings = []
        if lacheck:
            lacheck_count, lacheck_warnings = run_lacheck(tex_file)
            if lacheck_count > 0:
                total_warnings += lacheck_count

        file_results.append({
            'file': tex_file,
            'chktex_count': count,
            'chktex_warnings': warnings,
            'lacheck_count': lacheck_count,
            'lacheck_warnings': lacheck_warnings,
        })

        # Show warnings if verbose
        if verbose:
            for warning in warnings:
                console.print(f"  [yellow]{warning}[/yellow]")
            for warning in lacheck_warnings:
                console.print(f"  [cyan]{warning}[/cyan]")

    # Summary table
    console.print()
    table = Table(title="Lint Results")
    table.add_column("File", style="cyan")
    table.add_column("chktex", justify="right")
    if lacheck:
        table.add_column("lacheck", justify="right")

    for result in file_results:
        row = [
            str(result['file']),
            str(result['chktex_count']),
        ]
        if lacheck:
            row.append(str(result['lacheck_count']))
        table.add_row(*row)

    console.print(table)

    # Final summary
    console.print()
    if total_warnings == 0:
        console.print("[bold green]✓ No warnings found![/bold green]")
        sys.exit(0)
    else:
        color = "yellow" if not strict else "red"
        console.print(f"[bold {color}]Found {total_warnings} warning(s)[/bold {color}]")

        if not verbose:
            console.print("[dim]Run with --verbose to see all warnings[/dim]")

        if strict:
            sys.exit(1)
        sys.exit(0)


if __name__ == "__main__":
    main()
