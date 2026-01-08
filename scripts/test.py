#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "click>=8.0.0",
#   "rich>=13.0.0",
# ]
# ///
"""
Test runner for LaTeX Template Repository.

Runs tests inside Docker to verify the LaTeX setup works correctly.
No local LaTeX or act installation required - just Docker.

Usage:
    ./scripts/test.py
    ./scripts/test.py --test-doc tests/test_document.tex
    ./scripts/test.py --verbose
    make test
"""

import subprocess
import sys
import time
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


def run_in_docker(cmd: list[str], timeout: int = 300) -> tuple[bool, str, str]:
    """
    Run a command inside Docker container.

    Args:
        cmd: Command to run inside container
        timeout: Timeout in seconds

    Returns:
        Tuple of (success, stdout, stderr)
    """
    cwd = Path.cwd()
    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{cwd}:/workspace",
        "-w", "/workspace",
        DOCKER_IMAGE,
    ] + cmd

    try:
        result = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def test_latex_compilation(tex_file: Path, output_dir: Path, verbose: bool = False) -> tuple[bool, str]:
    """
    Test that a LaTeX file compiles successfully.

    Args:
        tex_file: Path to .tex file
        output_dir: Output directory for build artifacts
        verbose: Show verbose output

    Returns:
        Tuple of (success, message)
    """
    cmd = [
        "latexmk",
        "-pdf",
        "-shell-escape",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-g",  # Force rebuild (ignore cached state from previous errors)
        f"-output-directory={output_dir}",
        str(tex_file)
    ]

    success, stdout, stderr = run_in_docker(cmd, timeout=600)

    if verbose:
        if stdout:
            console.print(f"[dim]{stdout}[/dim]")

    if success:
        # Verify PDF was created
        pdf_name = tex_file.stem + ".pdf"
        pdf_path = output_dir / pdf_name
        if pdf_path.exists():
            size_kb = pdf_path.stat().st_size / 1024
            return True, f"PDF created ({size_kb:.1f} KB)"
        else:
            return False, "Compilation succeeded but PDF not found"
    else:
        # Extract error message
        output = stdout + stderr
        error_lines = []
        for line in output.split('\n'):
            if '!' in line or 'Error' in line or 'error' in line.lower():
                error_lines.append(line.strip())
        error_msg = '\n'.join(error_lines[-5:]) if error_lines else "Unknown error"
        return False, error_msg


def test_chktex_lint(tex_file: Path, verbose: bool = False) -> tuple[bool, str]:
    """
    Run chktex linter on a LaTeX file.

    Args:
        tex_file: Path to .tex file
        verbose: Show verbose output

    Returns:
        Tuple of (success, message)
    """
    cmd = ["chktex", "-q", str(tex_file)]

    success, stdout, stderr = run_in_docker(cmd, timeout=60)

    output = stdout + stderr
    warnings = [line for line in output.split('\n') if line.strip()]

    if verbose and warnings:
        for warning in warnings[:10]:
            console.print(f"[dim]  {warning}[/dim]")

    if not warnings:
        return True, "No warnings"
    else:
        return True, f"{len(warnings)} warning(s)"


def test_biber_available() -> tuple[bool, str]:
    """Test that biber is available in Docker."""
    cmd = ["biber", "--version"]
    success, stdout, _ = run_in_docker(cmd, timeout=30)

    if success:
        version = stdout.split('\n')[0] if stdout else "unknown"
        return True, version.strip()
    return False, "biber not found"


def test_pygments_available() -> tuple[bool, str]:
    """Test that Pygments is available for minted package."""
    cmd = ["python3", "-c", "import pygments; print(pygments.__version__)"]
    success, stdout, _ = run_in_docker(cmd, timeout=30)

    if success:
        version = stdout.strip()
        return True, f"v{version}"
    return False, "Pygments not found"


@click.command()
@click.option(
    '--test-doc', '-t',
    default='tests/test_document.tex',
    type=click.Path(path_type=Path),
    help='Test document to compile'
)
@click.option(
    '--output', '-o',
    default='build',
    type=click.Path(path_type=Path),
    help='Output directory for build artifacts'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Show verbose output'
)
@click.option(
    '--skip-compile', '-s',
    is_flag=True,
    help='Skip compilation test (faster)'
)
def main(test_doc: Path, output: Path, verbose: bool, skip_compile: bool):
    """
    Run tests to verify the LaTeX setup works correctly.

    All tests run inside Docker - no local LaTeX installation required.

    Tests include:
    - Docker image availability
    - biber (bibliography) availability
    - Pygments (minted syntax highlighting) availability
    - LaTeX compilation of test document
    - chktex linting
    """
    console.print(f"\n[bold blue]LaTeX Template Test Runner[/bold blue]")
    console.print(f"[dim]Docker image: {DOCKER_IMAGE}[/dim]\n")

    # Check Docker first
    if not check_docker_available():
        console.print("[red]✗ Docker is not available[/red]")
        console.print("Please start Docker and try again.")
        sys.exit(1)

    # Ensure output directory exists
    output.mkdir(parents=True, exist_ok=True)

    # Run tests
    results = []
    start_time = time.time()

    # Test 1: biber availability
    console.print("[dim]Testing biber availability...[/dim]")
    success, msg = test_biber_available()
    results.append(("biber available", success, msg))

    # Test 2: Pygments availability
    console.print("[dim]Testing Pygments availability...[/dim]")
    success, msg = test_pygments_available()
    results.append(("Pygments available", success, msg))

    # Test 3: Compile test document
    if not skip_compile:
        if test_doc.exists():
            console.print(f"[dim]Compiling {test_doc}...[/dim]")
            success, msg = test_latex_compilation(test_doc, output, verbose)
            results.append(("Test document compiles", success, msg))

            # Test 4: Lint test document
            console.print(f"[dim]Running chktex on {test_doc}...[/dim]")
            success, msg = test_chktex_lint(test_doc, verbose)
            results.append(("chktex lint", success, msg))
        else:
            results.append(("Test document compiles", False, f"File not found: {test_doc}"))
    else:
        console.print("[dim]Skipping compilation test[/dim]")

    elapsed = time.time() - start_time

    # Display results
    console.print()
    table = Table(title="Test Results")
    table.add_column("Test", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Details", style="dim")

    all_passed = True
    for test_name, success, message in results:
        status = "[green]✓ PASS[/green]" if success else "[red]✗ FAIL[/red]"
        if not success:
            all_passed = False
        table.add_row(test_name, status, message)

    console.print(table)
    console.print(f"\n[dim]Time: {elapsed:.1f}s[/dim]")

    # Summary
    console.print()
    if all_passed:
        console.print("[bold green]✓ All tests passed![/bold green]")
        sys.exit(0)
    else:
        console.print("[bold red]✗ Some tests failed[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
