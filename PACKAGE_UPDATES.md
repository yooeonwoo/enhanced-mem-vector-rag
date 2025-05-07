# Package Configuration Updates

## Summary of Changes

We've updated our package configuration to follow modern Python packaging best practices and simplify our development tooling. The key changes are:

1. **Moved dependencies to pyproject.toml**: All project dependencies are now defined in `pyproject.toml` instead of `requirements.txt`.
2. **Improved version specifiers**: Using `~=` version specifiers to allow patch updates while preventing breaking changes.
3. **Simplified tooling**: Consolidated formatting, linting, and import sorting with Ruff.
4. **Added development extras**: Development dependencies can now be installed with `pip install -e ".[dev]"`.
5. **Removed redundant tools**: Black and isort have been removed in favor of Ruff's formatter.

## Migration Guide

### Installing the Package

Instead of using `pip install -r requirements.txt`, you can now install the package with:

```bash
# For regular installation
pip install .

# For development installation with all development tools
pip install -e ".[dev]"
```

### Development Workflow

The development workflow has been simplified:

1. **Formatting and Linting**: Instead of running multiple tools, you can now use Ruff for both:
   ```bash
   # Format code including import sorting
   ruff format .
   
   # Lint code and fix common issues
   ruff check --fix .
   ```

2. **Pre-commit**: The pre-commit configuration has been updated to use Ruff for both formatting and linting.

3. **Type Checking**: The mypy configuration remains the same.

## Rationale for Changes

### Using pyproject.toml for Dependencies

PEP 621 standardized using pyproject.toml for package metadata, including dependencies. This provides several benefits:

- **Single source of truth**: All package configuration in one place
- **Proper dependency resolution**: Tools like pip can better resolve dependencies
- **Extras for optional dependencies**: Better management of dev and test dependencies

### Version Specifier Changes

We've switched from `>=` to `~=` version specifiers for most dependencies:

- `>=1.0.0` allows any version 1.0.0 or newer, which might break compatibility
- `~=1.0.0` allows patches (1.0.1, 1.0.2) but not minor/major updates (1.1.0, 2.0.0)

This helps prevent surprise breaking changes while still getting bug fixes.

### Consolidating Tools with Ruff

Ruff is a fast Python linter and formatter that can replace multiple tools:

- It's significantly faster than running flake8, black, and isort separately
- It provides consistent configuration in one place
- It supports import sorting natively, replacing isort
- It includes a formatter, replacing Black

## References

- [PEP 621 – Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Python Packaging User Guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)