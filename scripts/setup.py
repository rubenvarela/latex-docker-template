#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "rich>=13.0.0",
# ]
# ///
"""
Setup script for LaTeX Template Repository.

Verifies Docker is available and pulls the LaTeX image.
No local LaTeX installation required - everything runs in Docker.

Usage:
    ./scripts/setup.py
    make setup
"""

import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm

console = Console()

# Docker configuration
DOCKER_IMAGE = "texlive/texlive:latest-full"


def check_docker_installed() -> tuple[bool, str]:
    """Check if Docker is installed."""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, "Docker command failed"
    except (subprocess.SubprocessError, FileNotFoundError):
        return False, "Not found"


def check_docker_running() -> tuple[bool, str]:
    """Check if Docker daemon is running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return True, "Running"
        return False, "Daemon not running"
    except subprocess.SubprocessError:
        return False, "Could not connect"


def check_docker_image_exists() -> tuple[bool, str]:
    """Check if the LaTeX Docker image is already pulled."""
    try:
        result = subprocess.run(
            ["docker", "images", "-q", DOCKER_IMAGE],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return True, "Available locally"
        return False, "Not pulled yet"
    except subprocess.SubprocessError:
        return False, "Could not check"


def pull_docker_image() -> bool:
    """Pull the LaTeX Docker image."""
    console.print(f"\n[blue]Pulling {DOCKER_IMAGE}...[/blue]")
    console.print("[dim]This may take a few minutes (~4GB download)[/dim]\n")

    try:
        result = subprocess.run(
            ["docker", "pull", DOCKER_IMAGE],
            timeout=1800  # 30 minute timeout for large image
        )
        return result.returncode == 0
    except subprocess.SubprocessError as e:
        console.print(f"[red]Pull failed: {e}[/red]")
        return False


def check_optional_tool(name: str, flag: str = "--version") -> tuple[bool, str]:
    """Check if an optional tool is installed."""
    try:
        result = subprocess.run(
            [name, flag],
            capture_output=True,
            text=True,
            timeout=10
        )
        version = result.stdout.strip().split('\n')[0] if result.stdout else "Available"
        return True, version[:50]
    except (subprocess.SubprocessError, FileNotFoundError):
        return False, "Not found"


def create_directories() -> list[Path]:
    """Create required directories if they don't exist."""
    dirs = [
        Path("build"),
        Path("assets/images"),
        Path("assets/figures"),
        Path("tests/fixtures"),
    ]
    created = []
    for d in dirs:
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            created.append(d)
    return created


def main() -> int:
    """Main setup function."""
    console.print("\n[bold blue]LaTeX Template Repository Setup[/bold blue]")
    console.print("[dim]Docker-based builds - no local LaTeX required[/dim]\n")

    # ==========================================================================
    # Check Docker (Required)
    # ==========================================================================
    console.print("[bold]Checking Docker...[/bold]\n")

    table = Table(title="Docker Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status")
    table.add_column("Details")

    # Check Docker installed
    docker_installed, docker_version = check_docker_installed()
    if docker_installed:
        table.add_row("Docker CLI", "[green]✓ Installed[/green]", docker_version)
    else:
        table.add_row("Docker CLI", "[red]✗ Not found[/red]", "Required")
        console.print(table)
        console.print("\n[red]Docker is required for this project.[/red]")
        console.print("\nInstall Docker:")
        console.print("  macOS/Windows: https://www.docker.com/products/docker-desktop/")
        console.print("  Linux: https://docs.docker.com/engine/install/")
        return 1

    # Check Docker running
    docker_running, running_status = check_docker_running()
    if docker_running:
        table.add_row("Docker Daemon", "[green]✓ Running[/green]", running_status)
    else:
        table.add_row("Docker Daemon", "[red]✗ Not running[/red]", running_status)
        console.print(table)
        console.print("\n[red]Docker daemon is not running.[/red]")
        console.print("Please start Docker Desktop or the Docker daemon and try again.")
        return 1

    # Check image
    image_exists, image_status = check_docker_image_exists()
    if image_exists:
        table.add_row("LaTeX Image", "[green]✓ Available[/green]", DOCKER_IMAGE)
    else:
        table.add_row("LaTeX Image", "[yellow]○ Not pulled[/yellow]", DOCKER_IMAGE)

    console.print(table)

    # ==========================================================================
    # Pull Docker image if needed
    # ==========================================================================
    if not image_exists:
        console.print(f"\n[yellow]The LaTeX Docker image needs to be downloaded.[/yellow]")
        console.print(f"Image: {DOCKER_IMAGE}")
        console.print(f"Size: ~4GB\n")

        if Confirm.ask("Pull the image now?", default=True):
            if pull_docker_image():
                console.print("[green]✓ Image pulled successfully![/green]")
            else:
                console.print("[red]✗ Failed to pull image[/red]")
                console.print("You can pull it manually: docker pull " + DOCKER_IMAGE)
                return 1
        else:
            console.print("[yellow]Skipping image pull.[/yellow]")
            console.print(f"Run 'docker pull {DOCKER_IMAGE}' before building.")

    # ==========================================================================
    # Check optional tools
    # ==========================================================================
    console.print("\n[bold]Optional tools...[/bold]\n")

    opt_table = Table(title="Optional Tools (for advanced usage)")
    opt_table.add_column("Tool", style="cyan")
    opt_table.add_column("Status")
    opt_table.add_column("Purpose")

    optional_tools = [
        ("act", "--version", "Local GitHub Actions testing"),
        ("uv", "--version", "Python script runner"),
    ]

    for tool, flag, description in optional_tools:
        found, version = check_optional_tool(tool, flag)
        if found:
            opt_table.add_row(tool, "[green]✓ Found[/green]", description)
        else:
            opt_table.add_row(tool, "[dim]○ Not found[/dim]", description)

    console.print(opt_table)

    # ==========================================================================
    # Create directories
    # ==========================================================================
    console.print("\n[bold]Creating directories...[/bold]")
    created = create_directories()
    if created:
        for d in created:
            console.print(f"  [green]✓[/green] Created {d}")
    else:
        console.print("  [dim]All directories already exist[/dim]")

    # ==========================================================================
    # Summary
    # ==========================================================================
    console.print("\n" + "=" * 50)
    console.print("\n[bold green]✓ Setup complete![/bold green]")
    console.print("\nYou can now run:")
    console.print("  [cyan]make build[/cyan]      - Build the document (Docker)")
    console.print("  [cyan]make build-test[/cyan] - Build test document (Docker)")
    console.print("  [cyan]make watch[/cyan]      - Auto-rebuild on changes")
    console.print("  [cyan]make help[/cyan]       - See all available commands")

    return 0


if __name__ == "__main__":
    sys.exit(main())
