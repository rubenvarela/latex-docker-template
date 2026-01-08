#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "click>=8.0.0",
#   "rich>=13.0.0",
# ]
# ///
"""
Clean script for LaTeX Template Repository.

Removes build artifacts and auxiliary files generated during compilation.

Usage:
    ./scripts/clean.py
    ./scripts/clean.py --dry-run
    ./scripts/clean.py --all
    make clean
"""

import shutil
import sys
from pathlib import Path

import click
from rich.console import Console

console = Console()

# LaTeX auxiliary file extensions to clean
AUX_EXTENSIONS = {
    '.aux', '.bbl', '.bcf', '.blg', '.fdb_latexmk', '.fls',
    '.log', '.out', '.run.xml', '.synctex.gz', '.toc',
    '.lof', '.lot', '.nav', '.snm', '.vrb', '.idx',
    '.ilg', '.ind', '.glo', '.gls', '.glg', '.acn',
    '.acr', '.alg',
}

# Directories to clean
CLEAN_DIRS = [
    '_minted-*',  # Minted cache directories
]


def find_aux_files(directory: Path) -> list[Path]:
    """Find all auxiliary files in the given directory."""
    files = []
    if not directory.exists():
        return files

    for item in directory.rglob('*'):
        if item.is_file() and item.suffix in AUX_EXTENSIONS:
            files.append(item)

    return files


def find_minted_dirs(directory: Path) -> list[Path]:
    """Find all minted cache directories."""
    dirs = []
    if not directory.exists():
        return dirs

    for item in directory.glob('_minted-*'):
        if item.is_dir():
            dirs.append(item)

    # Also check in src directory
    src_dir = Path('src')
    if src_dir.exists():
        for item in src_dir.glob('_minted-*'):
            if item.is_dir():
                dirs.append(item)

    return dirs


def format_size(size_bytes: int) -> str:
    """Format byte size to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


@click.command()
@click.option(
    '--dry-run', '-n',
    is_flag=True,
    help='Show what would be deleted without actually deleting'
)
@click.option(
    '--all', '-a', 'clean_all',
    is_flag=True,
    help='Also clean the entire build directory and caches'
)
@click.option(
    '--build-dir', '-b',
    default='build',
    type=click.Path(path_type=Path),
    help='Build directory to clean'
)
def main(dry_run: bool, clean_all: bool, build_dir: Path):
    """
    Clean build artifacts and auxiliary files.

    Removes LaTeX auxiliary files (.aux, .log, .bbl, etc.) and
    minted cache directories.
    """
    console.print(f"\n[bold blue]LaTeX Clean[/bold blue]")

    if dry_run:
        console.print("[yellow]Dry run mode - no files will be deleted[/yellow]\n")

    files_to_delete: list[Path] = []
    dirs_to_delete: list[Path] = []
    total_size = 0

    # Find auxiliary files in src directory
    src_aux = find_aux_files(Path('src'))
    files_to_delete.extend(src_aux)

    # Find auxiliary files in build directory
    if build_dir.exists():
        build_aux = find_aux_files(build_dir)
        files_to_delete.extend(build_aux)

    # Find minted directories
    minted_dirs = find_minted_dirs(Path('.'))
    dirs_to_delete.extend(minted_dirs)

    # If --all, also delete entire build directory contents
    if clean_all and build_dir.exists():
        for item in build_dir.iterdir():
            if item.name != '.gitkeep':
                if item.is_file():
                    files_to_delete.append(item)
                elif item.is_dir():
                    dirs_to_delete.append(item)

    # Calculate total size
    for f in files_to_delete:
        try:
            total_size += f.stat().st_size
        except OSError:
            pass

    for d in dirs_to_delete:
        try:
            for item in d.rglob('*'):
                if item.is_file():
                    total_size += item.stat().st_size
        except OSError:
            pass

    # Report findings
    if not files_to_delete and not dirs_to_delete:
        console.print("[green]Nothing to clean![/green]")
        return

    console.print(f"Found {len(files_to_delete)} files and {len(dirs_to_delete)} directories")
    console.print(f"Total size: {format_size(total_size)}\n")

    # Delete files
    if files_to_delete:
        console.print("[bold]Files:[/bold]")
        for f in files_to_delete[:20]:  # Show first 20
            if dry_run:
                console.print(f"  [dim]Would delete:[/dim] {f}")
            else:
                try:
                    f.unlink()
                    console.print(f"  [red]Deleted:[/red] {f}")
                except OSError as e:
                    console.print(f"  [yellow]Failed:[/yellow] {f} ({e})")

        if len(files_to_delete) > 20:
            console.print(f"  [dim]... and {len(files_to_delete) - 20} more files[/dim]")

    # Delete directories
    if dirs_to_delete:
        console.print("\n[bold]Directories:[/bold]")
        for d in dirs_to_delete:
            if dry_run:
                console.print(f"  [dim]Would delete:[/dim] {d}/")
            else:
                try:
                    shutil.rmtree(d)
                    console.print(f"  [red]Deleted:[/red] {d}/")
                except OSError as e:
                    console.print(f"  [yellow]Failed:[/yellow] {d}/ ({e})")

    # Summary
    console.print()
    if dry_run:
        console.print(f"[yellow]Would free {format_size(total_size)}[/yellow]")
        console.print("[dim]Run without --dry-run to actually delete[/dim]")
    else:
        console.print(f"[green]✓ Cleaned {format_size(total_size)}[/green]")


if __name__ == "__main__":
    main()
