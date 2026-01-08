# =============================================================================
# Dockerfile - LaTeX Build Environment
# =============================================================================
# This Dockerfile creates a build environment for LaTeX documents.
# Based on texlive/texlive:latest-full for comprehensive package support.
#
# Usage:
#   docker build -t latex-template .
#   docker run --rm -v $(pwd):/workspace latex-template make build
# =============================================================================

FROM texlive/texlive:latest-full

# -----------------------------------------------------------------------------
# Labels
# -----------------------------------------------------------------------------
LABEL maintainer="Your Name <your.email@example.com>"
LABEL description="LaTeX document build environment"
LABEL version="1.0.0"

# -----------------------------------------------------------------------------
# System Dependencies
# -----------------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Python for scripts and Pygments (minted)
    python3 \
    python3-pip \
    python3-pygments \
    # Build tools
    make \
    # Git for version info
    git \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# Install uv for Python script management
# -----------------------------------------------------------------------------
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# -----------------------------------------------------------------------------
# Working Directory
# -----------------------------------------------------------------------------
WORKDIR /workspace

# -----------------------------------------------------------------------------
# Default Command
# -----------------------------------------------------------------------------
# Default to building the main document
CMD ["make", "build"]

# =============================================================================
# End of Dockerfile
# =============================================================================
