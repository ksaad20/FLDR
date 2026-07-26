# Contributing to FLDR

First off, thank you for your interest in contributing to **FLDR (Fault Line Detection in Robotics)**. Contributions of all sizes are welcome, whether they involve bug fixes, documentation improvements, new features, performance optimizations, or additional tests.

We aim to build a reliable, reproducible, and well-engineered open-source framework for fault detection and robotic inspection research.

---

# Table of Contents

- Ways to Contribute
- Development Setup
- Project Structure
- Coding Standards
- Testing
- Pull Request Process
- Reporting Bugs
- Requesting Features
- Documentation
- Community Standards
- License

---

# Ways to Contribute

You can contribute by:

- Fixing bugs
- Improving documentation
- Adding unit tests
- Improving code quality
- Implementing new algorithms
- Improving performance
- Adding examples
- Improving simulations
- Reporting issues
- Reviewing pull requests

---

# Development Setup

Clone the repository:

```bash
git clone https://github.com/ksaad20/FLDR.git
cd FLDR
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

Install FLDR in editable mode:

```bash
pip install -e .
```

Install development dependencies:

```bash
pip install -r requirements.txt
```

---

# Project Structure

```text
FLDR/
├── docs/
├── examples/
├── fldr/
├── tests/
├── .github/
├── docker/
├── README.md
├── LICENSE
├── pyproject.toml
└── mkdocs.yml
```

---

# Coding Standards

Please follow the project's coding style.

## Formatting

```bash
black .
```

## Linting

```bash
ruff check .
flake8 .
```

## Testing

```bash
pytest
```

## Coverage

```bash
pytest --cov=fldr --cov-report=xml
```

All GitHub Actions checks should pass before submitting a pull request.

---

# Writing Code

Please ensure that your contributions:

- Follow PEP 8
- Include type hints where practical
- Include docstrings for public APIs
- Keep functions focused and readable
- Avoid unnecessary dependencies
- Maintain backwards compatibility where possible

---

# Adding Tests

New features should include appropriate tests.

Tests belong in the `tests/` directory and should use `pytest`.

Example:

```python
def test_example():
    assert True
```

---

# Pull Request Process

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/my-feature
```

3. Make your changes.
4. Run formatting and tests.
5. Commit using clear commit messages.
6. Push your branch.
7. Open a Pull Request.

Please describe:

- What changed
- Why it changed
- Any relevant issues
- Testing performed

---

# Reporting Bugs

Please include:

- Operating system
- Python version
- FLDR version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Relevant logs or screenshots

---

# Feature Requests

Feature requests should describe:

- The problem being solved
- Proposed solution
- Alternative approaches considered
- Potential impact

---

# Documentation

Documentation improvements are always welcome.

This includes:

- API documentation
- Tutorials
- Examples
- Installation guides
- Developer documentation

---

# Community Standards

Please read and follow the project's
[Code of Conduct](CODE_OF_CONDUCT.md).

We are committed to maintaining a respectful, inclusive, and collaborative community.

---

# License

By contributing to FLDR, you agree that your contributions will be licensed under the **Apache License 2.0**.

---

# Questions

If you have questions, please open a GitHub Discussion or create an Issue.

Thank you for helping improve FLDR!
