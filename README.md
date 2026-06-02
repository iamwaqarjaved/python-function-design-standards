# Python Function Design Standards for Marketing Analytics Teams

A practical engineering handbook for writing clean, reviewable, testable Python functions in marketing analytics, data pipelines, reporting automation, and business intelligence workflows.

> **Purpose:** Help analytics teams turn scattered notebook logic into reliable, reusable Python functions.

---

## Why this guide exists

Marketing analytics code often starts in notebooks, spreadsheets, campaign exports, or quick scripts. That is normal. The problem begins when quick logic becomes production logic without standards.

Poorly designed functions can cause:

- Incorrect ROAS, CTR, CPA, or conversion-rate calculations
- Inconsistent UTM and campaign classification rules
- Duplicated dashboard logic across notebooks
- Hard-to-review pull requests
- Fragile ETL jobs and scheduled reports
- Business decisions based on unclear code

This repository provides a clear function-design standard that teams can adopt, teach, review against, and extend.

---

## What you will learn

By the end of this guide, you will understand how to design Python functions that are:

- **Readable:** names and signatures communicate intent
- **Reusable:** functions are small, focused, and business-aware
- **Reviewable:** reviewers can evaluate behavior quickly
- **Testable:** inputs and outputs are explicit
- **Maintainable:** business rules live in documented function boundaries

---

## Repository contents

| Path | Description |
|---|---|
| [`docs/function-design-standards.md`](docs/function-design-standards.md) | Full engineering handbook standard |
| [`examples/bad_vs_good_functions.py`](examples/bad_vs_good_functions.py) | Side-by-side examples of weak and improved function design |
| [`examples/marketing_metrics.py`](examples/marketing_metrics.py) | Practical reusable metric functions with type hints and docstrings |
| [`tests/test_marketing_metrics.py`](tests/test_marketing_metrics.py) | Example pytest tests for function behavior |
| [`CODE_REVIEW_CHECKLIST.md`](CODE_REVIEW_CHECKLIST.md) | 12-question function-level review checklist |
| [`.github/pull_request_template.md`](.github/pull_request_template.md) | PR checklist template for teams |

---

## Core standards covered

### 1. Naming standards

- Use `snake_case`
- Prefer verb-first names like `calculate_roas`, `normalize_campaign_name`, and `validate_utm_parameters`
- Keep each function focused on one responsibility
- Name functions after business intent, not implementation details

### 2. Signature standards

- Use positional arguments for required core inputs
- Use keyword-only arguments for options, flags, thresholds, date windows, and behavior modifiers
- Provide defaults only when the default is safe and business-approved
- Avoid `*args` and `**kwargs` unless forwarding to a stable external interface or building decorators

### 3. Type hints policy

- Required for public functions
- Optional for trivial private helpers
- Prefer modern Python syntax: `list[str]`, `dict[str, float]`, `str | None`
- Use precise domain types where helpful

### 4. Docstring standard

This guide uses **Google-style docstrings** because they are readable, compact, and suitable for mixed analytics/software teams.

### 5. Comprehension policy

Use comprehensions for simple transformations and filters. Avoid them when logic becomes deeply nested, multi-line, side-effect driven, or difficult to debug.

### 6. Lambda policy

Use `lambda` for short, local, single-use expressions such as sort keys. Replace lambdas with named functions when logic has business meaning, needs testing, or is reused.

---

## Quick example

### Weak function

```python
def roas(r, s):
    return r / s
```

Problems:

- Unclear parameter names
- No zero-spend handling
- No type hints
- No docstring
- Does not communicate business behavior

### Better function

```python
def calculate_roas(revenue: float, spend: float) -> float | None:
    """Calculate return on ad spend.

    Args:
        revenue: Revenue attributed to the campaign.
        spend: Advertising spend for the campaign.

    Returns:
        Revenue divided by spend, or None when spend is zero.
    """
    if spend == 0:
        return None

    return revenue / spend
```

This version is safer, reviewable, and easier to test.

---

## How to use this guide in a team

1. Add this repository to your team onboarding materials.
2. Use the checklist during pull request reviews.
3. Copy the PR template into analytics repositories.
4. Refactor notebook logic into functions that follow these standards.
5. Add tests for metric calculations, classification rules, and edge cases.

---

## Recommended workflow

```bash
# Clone the repository
git clone https://github.com/iamwaqarjaved/python-function-design-standards.git
cd python-function-design-standards

# Optional: create a virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows PowerShell

# Install test dependency
pip install pytest

# Run tests
pytest
```

---

## Who this is for

This guide is useful for:

- Marketing analytics engineers
- Data analysts learning production Python
- BI developers moving beyond dashboard-only logic
- Growth teams building reporting automation
- Students building credibility through technical documentation
- Junior developers preparing for code reviews

---

## Author

Created by **Waqar Javed** as a practical engineering handbook for Python function design standards.

---

## License

This project is provided for educational and professional portfolio use. Add a license such as MIT if you want others to reuse or adapt it formally.
