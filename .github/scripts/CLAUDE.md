# .github/scripts/ - GitHub-Specific Scripts

This directory contains scripts that run exclusively in GitHub Actions.

## Purpose

Store CI/CD automation scripts that are specific to GitHub workflows.

## When to Use This Directory

Put scripts here if they:
- Are only used in GitHub Actions workflows
- Require GitHub-specific environment variables
- Handle GitHub artifacts or releases
- Would not be useful locally

## When to Use scripts/ Instead

Put scripts in `scripts/` if they:
- Can be run locally
- Are useful for development
- Don't depend on GitHub environment

## Script Format

Same as `scripts/` - use uv inline metadata:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["click>=8.0.0"]
# ///

"""CI-specific script."""

import os

def main():
    # Access GitHub environment
    github_token = os.environ.get('GITHUB_TOKEN')
    github_ref = os.environ.get('GITHUB_REF')
    ...

if __name__ == "__main__":
    main()
```

## GitHub Environment Variables

Common variables available in workflows:
- `GITHUB_TOKEN` - Authentication token
- `GITHUB_REF` - Git ref (branch/tag)
- `GITHUB_SHA` - Commit SHA
- `GITHUB_REPOSITORY` - owner/repo
- `GITHUB_WORKSPACE` - Workspace path

## Example Scripts

### ci_build.py
Optimized build for CI environment with caching hints.

### release.py
Create GitHub releases with artifacts.

### validate.py
Validate build output for CI checks.

## Using in Workflows

In `.github/workflows/build.yml`:

```yaml
- name: Run CI script
  run: ./.github/scripts/ci_build.py
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Best Practices

1. **Handle missing variables**: Scripts should fail gracefully if env vars missing
2. **Log clearly**: CI output is important for debugging
3. **Exit codes**: Use proper exit codes for CI status
4. **Idempotent**: Scripts should be safe to re-run
