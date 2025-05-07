# Contributing to Enhanced Memory Vector RAG

Thank you for your interest in contributing to Enhanced Memory Vector RAG (EMVR)! This document outlines the process for contributing to the project and helps ensure a smooth collaboration experience.

## Table of Contents

- [Contributing to Enhanced Memory Vector RAG](#contributing-to-enhanced-memory-vector-rag)
  - [Table of Contents](#table-of-contents)
  - [Code of Conduct](#code-of-conduct)
  - [Getting Started](#getting-started)
  - [Development Workflow](#development-workflow)
  - [Pull Request Process](#pull-request-process)
  - [Coding Standards](#coding-standards)
  - [Testing Guidelines](#testing-guidelines)
  - [Documentation](#documentation)
  - [Issue Reporting](#issue-reporting)
  - [Feature Requests](#feature-requests)
  - [Community](#community)

## Code of Conduct

This project adheres to a Code of Conduct that establishes expected behavior in our community. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

To get started with contributing to EMVR:

1. Fork the repository
2. Clone your fork locally
3. Set up the development environment:

   ```bash
   # Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate

   # Install development dependencies
   pip install -e ".[dev]"
   ```

4. Create a new branch for your feature or bugfix:

   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

1. Make your changes in small, incremental commits
2. Keep your branch updated with the main repository:

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

3. Run tests locally before submitting a pull request:

   ```bash
   pytest
   ```

4. Update documentation as needed

## Pull Request Process

1. Ensure your code passes all tests and linting checks
2. Update the README.md or documentation with details of changes if appropriate
3. Submit a pull request to the `main` branch with a clear description of the changes
4. Respond to any feedback or requests for changes
5. Once approved, your pull request will be merged

## Coding Standards

- Follow PEP 8 guidelines for Python code
- Use type hints where appropriate
- Format your code using Black with the default settings
- Use descriptive variable and function names
- Comment complex code sections

## Testing Guidelines

- Write unit tests for all new functionality
- Ensure existing tests pass with your changes
- Include integration tests for complex features
- Document test cases with clear descriptions

## Documentation

- Update documentation for any changes to the API
- Document new features thoroughly
- Include docstrings for all public functions and classes
- Provide examples for new features

## Issue Reporting

When reporting issues:

1. Use the issue template provided
2. Include a clear description of the issue
3. Provide steps to reproduce the problem
4. Include information about your environment
5. If possible, suggest a solution

## Feature Requests

When suggesting new features:

1. Check if the feature has already been suggested
2. Provide a clear description of the feature
3. Explain the use case and benefits
4. Consider implementation details if possible

## Community

- Join our community discussions
- Help answer questions from other users
- Share your experiences and use cases
- Provide feedback on new features and releases

Thank you for contributing to Enhanced Memory Vector RAG!
