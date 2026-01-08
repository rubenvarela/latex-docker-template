#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "click>=8.0.0",
#   "rich>=13.0.0",
#   "watchdog>=3.0.0",
# ]
# ///
"""
Watch mode for LaTeX Template Repository.

Watches for file changes and automatically triggers a rebuild using Docker.
No local LaTeX installation required.

Usage:
    ./scripts/watch.py --src src --output build
    ./scripts/watch.py --src src --local  # Use local LaTeX
    make watch
"""

import subprocess
import sys
import time
from pathlib import Path

import click
from rich.console import Console
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

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


class LaTeXHandler(FileSystemEventHandler):
    """Handler for LaTeX file changes."""

    def __init__(
        self,
        src_dir: Path,
        output_dir: Path,
        main_file: str,
        use_local: bool = False,
        debounce_seconds: float = 1.0
    ):
        self.src_dir = src_dir
        self.output_dir = output_dir
        self.main_file = main_file
        self.use_local = use_local
        self.debounce_seconds = debounce_seconds
        self.last_build_time = 0
        self.building = False

        # File extensions to watch
        self.watch_extensions = {'.tex', '.bib', '.sty', '.cls'}

    def should_rebuild(self, event: FileSystemEvent) -> bool:
        """Determine if we should rebuild based on the event."""
        if self.building:
            return False

        # Get file extension
        path = Path(event.src_path)
        if path.suffix not in self.watch_extensions:
            return False

        # Ignore files in build directory
        try:
            path.relative_to(self.output_dir)
            return False
        except ValueError:
            pass

        # Debounce
        current_time = time.time()
        if current_time - self.last_build_time < self.debounce_seconds:
            return False

        return True

    def rebuild(self):
        """Trigger a rebuild using Docker or local LaTeX."""
        self.building = True
        self.last_build_time = time.time()

        console.print(f"\n[blue]Rebuilding...[/blue]")

        main_tex = self.src_dir / self.main_file
        cwd = Path.cwd()

        try:
            if self.use_local:
                # Local build
                result = subprocess.run(
                    [
                        "latexmk",
                        "-pdf",
                        "-shell-escape",
                        "-interaction=nonstopmode",
                        f"-output-directory={self.output_dir}",
                        str(main_tex)
                    ],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
            else:
                # Docker build
                result = subprocess.run(
                    [
                        "docker", "run", "--rm",
                        "-v", f"{cwd}:/workspace",
                        "-w", "/workspace",
                        DOCKER_IMAGE,
                        "latexmk",
                        "-pdf",
                        "-shell-escape",
                        "-interaction=nonstopmode",
                        f"-output-directory={self.output_dir}",
                        str(main_tex)
                    ],
                    capture_output=True,
                    text=True,
                    timeout=300
                )

            if result.returncode == 0:
                console.print(f"[green]✓ Build successful![/green]")
            else:
                console.print(f"[red]✗ Build failed[/red]")
                # Show last few lines of error
                output = result.stdout + result.stderr
                error_lines = output.strip().split('\n')[-5:]
                for line in error_lines:
                    if line.strip():
                        console.print(f"  [dim]{line}[/dim]")

        except subprocess.TimeoutExpired:
            console.print(f"[red]✗ Build timed out[/red]")
        except Exception as e:
            console.print(f"[red]✗ Error: {e}[/red]")
        finally:
            self.building = False

        console.print(f"\n[dim]Watching for changes... (Ctrl+C to stop)[/dim]")

    def on_modified(self, event: FileSystemEvent):
        if not event.is_directory and self.should_rebuild(event):
            console.print(f"[dim]Changed: {event.src_path}[/dim]")
            self.rebuild()

    def on_created(self, event: FileSystemEvent):
        if not event.is_directory and self.should_rebuild(event):
            console.print(f"[dim]Created: {event.src_path}[/dim]")
            self.rebuild()


@click.command()
@click.option(
    '--src', '-s',
    default='src',
    type=click.Path(exists=True, path_type=Path),
    help='Source directory to watch'
)
@click.option(
    '--output', '-o',
    default='build',
    type=click.Path(path_type=Path),
    help='Output directory for build artifacts'
)
@click.option(
    '--main', '-m',
    default='main.tex',
    help='Main .tex file to compile'
)
@click.option(
    '--debounce', '-d',
    default=1.0,
    type=float,
    help='Minimum seconds between rebuilds'
)
@click.option(
    '--local', '-l',
    is_flag=True,
    help='Use local LaTeX installation instead of Docker'
)
@click.option(
    '--initial-build/--no-initial-build',
    default=True,
    help='Perform an initial build when starting'
)
def main(src: Path, output: Path, main: str, debounce: float, local: bool, initial_build: bool):
    """
    Watch for file changes and auto-rebuild using Docker.

    Monitors the source directory for changes to .tex, .bib, .sty, and .cls
    files and automatically triggers a rebuild when changes are detected.

    By default, builds run in Docker. Use --local for local LaTeX.
    """
    console.print(f"\n[bold blue]LaTeX Watch Mode[/bold blue]")
    console.print(f"Source: {src}")
    console.print(f"Output: {output}")
    console.print(f"Main file: {main}")

    if local:
        console.print("[yellow]Mode: Local LaTeX[/yellow]")
    else:
        console.print(f"[dim]Docker image: {DOCKER_IMAGE}[/dim]")

    console.print(f"Debounce: {debounce}s\n")

    # Check Docker if not using local
    if not local:
        if not check_docker_available():
            console.print("[red]✗ Docker is not available[/red]")
            console.print("Please start Docker or use --local for local builds")
            sys.exit(1)

    # Ensure output directory exists
    output.mkdir(parents=True, exist_ok=True)

    # Create handler and observer
    handler = LaTeXHandler(src, output, main, local, debounce)
    observer = Observer()

    # Watch source directory
    observer.schedule(handler, str(src), recursive=True)

    # Also watch styles directory if it exists
    styles_dir = Path("styles")
    if styles_dir.exists():
        observer.schedule(handler, str(styles_dir), recursive=True)

    # Also watch assets directory
    assets_dir = Path("assets")
    if assets_dir.exists():
        observer.schedule(handler, str(assets_dir), recursive=True)

    observer.start()

    console.print("[green]✓ Watch mode started[/green]")
    console.print(f"[dim]Watching for changes... (Ctrl+C to stop)[/dim]")

    # Initial build if requested
    if initial_build:
        handler.rebuild()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopping watch mode...[/yellow]")
        observer.stop()

    observer.join()
    console.print("[green]✓ Watch mode stopped[/green]")


if __name__ == "__main__":
    main()
