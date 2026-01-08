#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "click>=8.0.0",
#   "rich>=13.0.0",
# ]
# ///
"""
Build script for LaTeX documents using Docker.

Compiles LaTeX documents inside a Docker container for reproducibility.
No local LaTeX installation required.

Usage:
    ./scripts/build.py --src src/main.tex --output build
    ./scripts/build.py --src src/main.tex --draft
    ./scripts/build.py --src src/main.tex --local  # Use local LaTeX
    make build
"""

import os
import subprocess
import sys
import time
from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

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


def run_docker_build(
    src: Path,
    output_dir: Path,
    draft: bool = False,
    validate_only: bool = False
) -> tuple[bool, str]:
    """
    Run build inside Docker container.

    Args:
        src: Path to the main .tex file
        output_dir: Directory for output files
        draft: If True, do a quick single-pass build
        validate_only: If True, only check syntax

    Returns:
        Tuple of (success, output_message)
    """
    # Get the current working directory for volume mount
    cwd = Path.cwd()

    # Build the latexmk command to run inside Docker
    latex_cmd = [
        "latexmk",
        "-pdf",
        "-shell-escape",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-g",  # Force rebuild (ignore cached state from previous errors)
        f"-output-directory={output_dir}",
    ]

    if draft:
        latex_cmd.append("-pdflatex=pdflatex -shell-escape -draftmode %O %S")

    if validate_only:
        latex_cmd.extend([
            "-pdflatex=pdflatex -shell-escape -draftmode -halt-on-error %O %S",
            "-g"
        ])

    latex_cmd.append(str(src))

    # Build the Docker command
    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{cwd}:/workspace",
        "-w", "/workspace",
        DOCKER_IMAGE,
    ] + latex_cmd

    try:
        result = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )

        if result.returncode == 0:
            return True, "Build successful"
        else:
            # Extract error message from output
            output = result.stdout + result.stderr
            error_lines = []
            for line in output.split('\n'):
                if '!' in line or 'Error' in line or 'error' in line.lower():
                    error_lines.append(line)

            error_msg = '\n'.join(error_lines[-10:]) if error_lines else output[-1000:]
            return False, error_msg

    except subprocess.TimeoutExpired:
        return False, "Build timed out after 10 minutes"
    except FileNotFoundError:
        return False, "Docker not found. Please install Docker."
    except Exception as e:
        return False, f"Unexpected error: {e}"


def run_local_build(
    src: Path,
    output_dir: Path,
    draft: bool = False,
    validate_only: bool = False
) -> tuple[bool, str]:
    """
    Run build using local LaTeX installation.

    Args:
        src: Path to the main .tex file
        output_dir: Directory for output files
        draft: If True, do a quick single-pass build
        validate_only: If True, only check syntax

    Returns:
        Tuple of (success, output_message)
    """
    cmd = [
        "latexmk",
        "-pdf",
        "-shell-escape",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-g",  # Force rebuild (ignore cached state from previous errors)
        f"-output-directory={output_dir}",
    ]

    if draft:
        cmd.append("-pdflatex=pdflatex -shell-escape -draftmode %O %S")

    if validate_only:
        cmd.extend([
            "-pdflatex=pdflatex -shell-escape -draftmode -halt-on-error %O %S",
            "-g"
        ])

    cmd.append(str(src))

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            return True, "Build successful"
        else:
            error_lines = []
            for line in result.stdout.split('\n'):
                if '!' in line or 'Error' in line:
                    error_lines.append(line)

            error_msg = '\n'.join(error_lines[-10:]) if error_lines else result.stdout[-500:]
            return False, error_msg

    except subprocess.TimeoutExpired:
        return False, "Build timed out after 5 minutes"
    except FileNotFoundError:
        return False, "latexmk not found. Install TeX Live or use Docker (remove --local)."
    except Exception as e:
        return False, f"Unexpected error: {e}"


def get_pdf_path(src: Path, output_dir: Path) -> Path:
    """Get the expected PDF output path."""
    return output_dir / src.with_suffix('.pdf').name


@click.command()
@click.option(
    '--src', '-s',
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help='Source .tex file to compile'
)
@click.option(
    '--output', '-o',
    default='build',
    type=click.Path(path_type=Path),
    help='Output directory for build artifacts'
)
@click.option(
    '--draft', '-d',
    is_flag=True,
    help='Quick draft build (single pass, no bibliography)'
)
@click.option(
    '--validate-only', '-v',
    is_flag=True,
    help='Only validate syntax without full compilation'
)
@click.option(
    '--local', '-l',
    is_flag=True,
    help='Use local LaTeX installation instead of Docker'
)
@click.option(
    '--clean', '-c',
    is_flag=True,
    help='Clean auxiliary files before building'
)
def main(src: Path, output: Path, draft: bool, validate_only: bool, local: bool, clean: bool):
    """
    Build a LaTeX document using Docker.

    By default, builds run inside a Docker container with a full TeX Live
    installation. Use --local to build with a local LaTeX installation.
    """
    console.print(f"\n[bold blue]LaTeX Build[/bold blue]")
    console.print(f"Source: {src}")
    console.print(f"Output: {output}")

    if local:
        console.print("[yellow]Mode: Local LaTeX[/yellow]")
    else:
        console.print(f"[dim]Docker image: {DOCKER_IMAGE}[/dim]")

    if draft:
        console.print("[yellow]Mode: Draft (single pass)[/yellow]")
    elif validate_only:
        console.print("[yellow]Mode: Validation only[/yellow]")

    # Check Docker if not using local
    if not local:
        if not check_docker_available():
            console.print("\n[red]✗ Docker is not available[/red]")
            console.print("Please start Docker or use --local for local builds")
            sys.exit(1)

    # Ensure output directory exists
    output.mkdir(parents=True, exist_ok=True)

    # Clean if requested (run in Docker too for consistency)
    if clean:
        console.print("\n[dim]Cleaning auxiliary files...[/dim]")
        if local:
            subprocess.run(
                ["latexmk", "-c", f"-output-directory={output}", str(src)],
                capture_output=True
            )
        else:
            cwd = Path.cwd()
            subprocess.run([
                "docker", "run", "--rm",
                "-v", f"{cwd}:/workspace",
                "-w", "/workspace",
                DOCKER_IMAGE,
                "latexmk", "-c", f"-output-directory={output}", str(src)
            ], capture_output=True)

    # Build with progress indicator
    console.print()
    start_time = time.time()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        if local:
            task = progress.add_task("Compiling (local)...", total=None)
            success, message = run_local_build(src, output, draft, validate_only)
        else:
            task = progress.add_task("Compiling in Docker...", total=None)
            success, message = run_docker_build(src, output, draft, validate_only)
        progress.update(task, completed=True)

    elapsed = time.time() - start_time

    # Report results
    console.print()
    if success:
        pdf_path = get_pdf_path(src, output)
        console.print(f"[bold green]✓ Build successful![/bold green]")
        console.print(f"  Output: {pdf_path}")
        console.print(f"  Time: {elapsed:.1f}s")

        if pdf_path.exists():
            size_mb = pdf_path.stat().st_size / (1024 * 1024)
            console.print(f"  Size: {size_mb:.2f} MB")

        sys.exit(0)
    else:
        console.print(f"[bold red]✗ Build failed![/bold red]")
        console.print(f"\n[dim]Error output:[/dim]")
        console.print(message)
        console.print(f"\n[dim]Check the full log at: {output}/{src.stem}.log[/dim]")
        sys.exit(1)


if __name__ == "__main__":
    main()
