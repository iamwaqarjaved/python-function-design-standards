# Function Design Standards for the Marketing Analytics Team

**Document type:** Engineering Handbook Standard  
**Audience:** Marketing analytics engineers, data analysts, analytics developers, and code reviewers  
**Primary language:** Python 3.11+  
**Adopted style:** PEP 8 naming conventions, Google-style docstrings, explicit type hints for public functions  

---

## 1. Executive Summary

This document defines the function-design standards used by the marketing analytics team when writing Python code for campaign reporting, attribution analysis, customer segmentation, ETL workflows, dashboard data preparation, experimentation analysis, and marketing performance automation.

The goal is not to make every function look identical. The goal is to make every function easy to read, easy to test, easy to review, and safe to reuse. A good function should communicate its purpose through its name, accept inputs through a clear signature, return predictable outputs, and avoid hidden behavior. For a marketing analytics team, this matters because small function-level ambiguity can create large business-level errors: misclassified campaigns, duplicated conversions, incorrect ROAS calculations, wrong attribution windows, or misleading dashboard numbers.

These standards apply to all production Python code owned by the team, including scripts, notebooks that are promoted into reusable modules, scheduled jobs, shared utility packages, and analytics libraries. Exploratory notebooks may be less formal, but any logic that becomes shared or operational must follow this standard.

---

## 2. Guiding Principles

Function design should be guided by the following principles.

### 2.1 Functions should be readable before they are clever

Marketing analytics code is frequently reviewed by people with mixed backgrounds: software engineers, data analysts, BI developers, marketing operations specialists, and analytics managers. A function that is technically compact but hard to understand increases operational risk. Prefer simple control flow, explicit names, and clear return values over dense expressions.

### 2.2 Functions should do one job

A function should have one primary responsibility. If a function loads campaign data, cleans it, aggregates it, calculates metrics, writes a file, and sends an alert, it is too broad. Split the workflow into smaller functions with names that describe each step.

### 2.3 Function boundaries should protect business meaning

Analytics code often contains business rules: attribution windows, channel grouping, paid-versus-organic classification, campaign naming conventions, and currency handling. These rules should be placed in named, documented functions rather than scattered across notebooks or inline lambda expressions.

### 2.4 Function behavior should be testable

A reviewer should be able to understand what inputs a function expects, what it returns, and which edge cases must be tested. Functions that depend on global variables, hidden state, current dates, environment variables, or live APIs are harder to test and should isolate those dependencies.

---

## 3. Scope and Applicability

This standard applies to:

- Public functions in shared modules.
- Private helper functions inside production modules.
- Functions used in ETL pipelines and scheduled reporting jobs.
- Functions used for campaign classification, metric calculations, data validation, and transformations.
- Reusable functions extracted from notebooks.
- Functions included in internal packages or shared repositories.

This standard does not require full production-level documentation for every short exploratory function in an analysis notebook. However, once a function is reused, copied across projects, reviewed in a pull request, or scheduled in an automated workflow, it should follow this document.

---

## 4. Naming Standards

### 4.1 Use `snake_case` for all function names

All Python function names must use lowercase words separated by underscores.

**Correct:**

```python
def calculate_roas(revenue: float, spend: float) -> float:
    ...


def normalize_campaign_name(name: str) -> str:
    ...
```

**Incorrect:**

```python
def calculateROAS(revenue, spend):
    ...


def NormalizeCampaignName(name):
    ...
```

Function names should be readable when spoken aloud. Avoid unnecessary abbreviations unless the abbreviation is standard in the team’s business domain.

Acceptable domain abbreviations include:

- `roas` for return on ad spend.
- `ctr` for click-through rate.
- `cpc` for cost per click.
- `cpm` for cost per mille.
- `utm` for Urchin Tracking Module parameters.
- `kpi` for key performance indicator.

Avoid unclear abbreviations such as `calc_m`, `proc_df`, `fix_vals`, or `do_stuff`.

---

### 4.2 Prefer verb-first names for functions

Function names should normally begin with a verb because functions do work. The verb should describe the action, and the rest of the name should describe the object or business concept.

Recommended verbs:

| Verb | Use when the function... | Example |
|---|---|---|
| `calculate_` | Computes a metric or derived value | `calculate_conversion_rate` |
| `normalize_` | Standardizes format or casing | `normalize_campaign_name` |
| `validate_` | Checks input against rules and raises or returns validation results | `validate_utm_parameters` |
| `parse_` | Converts raw text into structured values | `parse_campaign_code` |
| `extract_` | Pulls fields from a larger object | `extract_utm_source` |
| `filter_` | Selects a subset of records | `filter_paid_campaigns` |
| `map_` | Converts values using a mapping rule | `map_channel_group` |
| `aggregate_` | Summarizes data | `aggregate_daily_spend` |
| `format_` | Converts output into display-ready form | `format_currency_value` |
| `load_` | Reads data from a source | `load_campaign_spend` |
| `write_` | Writes data to a destination | `write_report_csv` |
| `build_` | Constructs a structured object | `build_attribution_summary` |
| `send_` | Sends a notification, file, or request | `send_budget_alert` |

**Good:**

```python
def calculate_ctr(clicks: int, impressions: int) -> float:
    ...
```

**Weak:**

```python
def ctr(clicks: int, impressions: int) -> float:
    ...
```

The weak version is concise but less clear. It does not reveal whether the function calculates, formats, validates, or retrieves CTR.

---

### 4.3 Name functions after business intent, not implementation details

A function name should explain why the function exists, not merely how it works internally.

**Preferred:**

```python
def classify_marketing_channel(source: str, medium: str) -> str:
    ...
```

**Avoid:**

```python
def apply_source_medium_if_else(source: str, medium: str) -> str:
    ...
```

Implementation details can change. Business intent should remain stable.

---

### 4.4 Use the single-responsibility principle

Each function should have one reason to change. If the business rule changes, only the function responsible for that rule should need modification. If the output format changes, only formatting functions should change. If the data source changes, only loading functions should change.

**Too broad:**

```python
def create_weekly_paid_report(start_date, end_date):
    data = download_ads_data(start_date, end_date)
    data = clean_ads_data(data)
    summary = calculate_metrics(data)
    chart = create_chart(summary)
    send_email(chart)
```

This function mixes data access, cleaning, metric calculation, visualization, and notification.

**Better:**

```python
def create_weekly_paid_report(start_date: str, end_date: str) -> None:
    raw_data = load_ads_data(start_date, end_date)
    clean_data = clean_ads_data(raw_data)
    summary = calculate_paid_media_metrics(clean_data)
    report = build_weekly_report(summary)
    send_report_email(report)
```

The orchestrating function may call several steps, but each step is isolated behind a named function. This makes review, testing, and debugging easier.

---

## 5. Signature Standards

A function signature is a contract. It tells callers what information is required, which values are optional, and how the function should be used. Poor signatures cause misuse, unexpected behavior, and brittle code.

---

### 5.1 Use positional arguments for required, obvious inputs

Use positional arguments when the argument meaning is obvious from the function name and order.

```python
def calculate_roas(revenue: float, spend: float) -> float:
    if spend == 0:
        return 0.0
    return revenue / spend
```

Calling this function is readable:

```python
roas = calculate_roas(12500.0, 4200.0)
```

However, positional arguments become risky when multiple arguments have the same type or similar meaning.

---

### 5.2 Use keyword-only arguments for configuration and business rules

Keyword-only arguments should be used for optional settings, flags, thresholds, attribution windows, date boundaries, and any value where the caller should be explicit.

Use `*` in the function signature to force later arguments to be passed by keyword.

```python
def calculate_attributed_revenue(
    conversions: list[dict],
    *,
    attribution_window_days: int = 30,
    include_view_through: bool = False,
) -> float:
    ...
```

Correct call:

```python
revenue = calculate_attributed_revenue(
    conversions,
    attribution_window_days=14,
    include_view_through=True,
)
```

Incorrect call:

```python
revenue = calculate_attributed_revenue(conversions, 14, True)
```

The incorrect call hides business meaning. A reviewer cannot tell what `14` and `True` represent without checking the function definition.

---

### 5.3 Provide defaults only when the default is safe and business-approved

Defaults should not be added merely for convenience. A default value becomes a business assumption. For example, a default attribution window of 30 days may be correct for one platform but wrong for another.

Good defaults are:

- Stable across most use cases.
- Safe if the caller forgets to override them.
- Documented in the docstring.
- Covered by tests.

**Acceptable:**

```python
def normalize_campaign_name(name: str, *, lowercase: bool = True) -> str:
    ...
```

**Risky:**

```python
def calculate_ltv(customer_id: str, months: int = 12) -> float:
    ...
```

The second example may be risky because the correct LTV window is usually a business decision. The caller should be forced to specify it unless the team has formally standardized the default.

---

### 5.4 Avoid mutable default arguments

Never use mutable objects such as lists, dictionaries, or sets as default argument values.

**Incorrect:**

```python
def add_campaign_tag(campaign: dict, tags: list[str] = []) -> dict:
    tags.append("paid")
    campaign["tags"] = tags
    return campaign
```

Mutable defaults are created once when the function is defined, not each time it is called. This can cause values to leak between calls.

**Correct:**

```python
def add_campaign_tag(campaign: dict, tags: list[str] | None = None) -> dict:
    resolved_tags = [] if tags is None else list(tags)
    resolved_tags.append("paid")
    campaign["tags"] = resolved_tags
    return campaign
```

---

### 5.5 Use `*args` sparingly

Use `*args` only when the function naturally accepts a variable number of positional values and those values have the same meaning.

Acceptable example:

```python
def combine_campaign_ids(*campaign_ids: str) -> str:
    return ",".join(campaign_ids)
```

Avoid `*args` when the arguments have different meanings.

**Incorrect:**

```python
def create_report(*args):
    start_date = args[0]
    end_date = args[1]
    channel = args[2]
```

This hides the contract and makes the function hard to use safely.

---

### 5.6 Use `**kwargs` only for controlled pass-through or extensibility

`**kwargs` should not be used as a shortcut to avoid designing a clear function signature. It is acceptable when passing through configuration to a well-defined downstream library or when implementing a wrapper around a stable interface.

Acceptable example:

```python
def read_csv_report(path: str, **read_csv_options) -> "pd.DataFrame":
    return pd.read_csv(path, **read_csv_options)
```

Even in this case, the docstring must explain which keyword arguments are expected or where they are passed.

Avoid:

```python
def calculate_metrics(data, **kwargs):
    if kwargs.get("use_net_revenue"):
        ...
    if kwargs.get("include_tax"):
        ...
```

This design hides important business rules. Use explicit keyword-only arguments instead.

---

### 5.7 Prefer returning values over mutating inputs

Unless the function name clearly indicates mutation, functions should return new values instead of modifying input objects in place.

**Preferred:**

```python
def add_roas_column(df: "pd.DataFrame") -> "pd.DataFrame":
    result = df.copy()
    result["roas"] = result["revenue"] / result["spend"]
    return result
```

**Risky:**

```python
def add_roas_column(df: "pd.DataFrame") -> None:
    df["roas"] = df["revenue"] / df["spend"]
```

In-place mutation can be acceptable for performance-sensitive data processing, but the function name and docstring must make the behavior explicit.

---

## 6. Type Hints Policy

Type hints make function contracts visible to humans and tools. They improve autocomplete, static analysis, review quality, and long-term maintainability.

---

### 6.1 Type hints are required for public functions

Every public function in a shared module must include type hints for all parameters and the return value.

A public function is any function that:

- Is imported by another module.
- Is used by scheduled jobs.
- Is used by dashboards or reporting workflows.
- Encodes a business rule.
- Is intended for reuse by other team members.

Example:

```python
def calculate_conversion_rate(conversions: int, sessions: int) -> float:
    if sessions == 0:
        return 0.0
    return conversions / sessions
```

---

### 6.2 Type hints are optional for trivial private helpers

Private helper functions begin with a single underscore. Type hints are optional only when the helper is extremely small, local to one module, and obvious.

Acceptable:

```python
def _strip(value):
    return value.strip()
```

Preferred when the helper is reused or business-relevant:

```python
def _strip_campaign_prefix(name: str) -> str:
    return name.removeprefix("campaign_")
```

When in doubt, add type hints.

---

### 6.3 Use modern collection syntax

Use built-in generic collection syntax such as `list[str]`, `dict[str, float]`, and `tuple[str, int]`.

```python
def get_active_campaign_ids(campaigns: list[dict[str, object]]) -> list[str]:
    ...
```

Avoid older `typing.List` and `typing.Dict` unless the codebase must support older Python versions.

---

### 6.4 Use `| None` instead of `Optional` in Python 3.10+

Use the union operator for nullable values.

Preferred:

```python
def find_campaign_owner(campaign_id: str) -> str | None:
    ...
```

Acceptable only for legacy consistency:

```python
from typing import Optional


def find_campaign_owner(campaign_id: str) -> Optional[str]:
    ...
```

A nullable type means the function may return `None`. It does not mean the parameter is optional in the function call. If a parameter has no default value, callers must still provide it.

---

### 6.5 Use union types only when the function truly accepts multiple types

Use `str | Path` when the function is intentionally designed to accept either type.

```python
from pathlib import Path


def load_campaign_config(path: str | Path) -> dict[str, object]:
    ...
```

Do not use broad unions to hide inconsistent upstream data. Normalize data before passing it into business logic functions.

Avoid:

```python
def calculate_spend(spend: int | float | str | None) -> float:
    ...
```

Prefer:

```python
def parse_spend(value: str | None) -> float:
    ...


def calculate_spend(spend: float) -> float:
    ...
```

Separate parsing from calculation.

---

### 6.6 Avoid `Any` unless there is a clear reason

`Any` disables type checking for that value. It should be rare in production code.

Acceptable uses include:

- JSON-like external API payloads before validation.
- Temporary compatibility with third-party libraries that lack useful types.
- Generic utility functions where the type is genuinely unconstrained.

When using `Any`, keep it near the boundary of the system and convert it into typed structures as soon as practical.

---

### 6.7 Prefer typed domain objects for complex data

When passing complex dictionaries across multiple functions, consider using a `dataclass`, `TypedDict`, or Pydantic model depending on the project.

Dictionary-heavy code becomes hard to review because keys, required fields, and value types are not obvious.

Weak:

```python
def calculate_campaign_margin(campaign: dict[str, object]) -> float:
    return campaign["revenue"] - campaign["cost"]
```

Better:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class CampaignMetrics:
    campaign_id: str
    revenue: float
    cost: float


def calculate_campaign_margin(metrics: CampaignMetrics) -> float:
    return metrics.revenue - metrics.cost
```

---

## 7. Docstring Standard

The team uses **Google-style docstrings**.

Google-style docstrings are readable in plain text, concise enough for normal development, and compatible with common documentation tools. Every public function must include a docstring unless the function is extremely simple and its behavior is fully obvious from the name, signature, and return type. Business-rule functions should always have docstrings.

---

### 7.1 Required docstring sections

A standard docstring should include:

1. One-sentence summary.
2. Additional detail when the function contains business rules or non-obvious behavior.
3. `Args:` section for parameters.
4. `Returns:` section for return value.
5. `Raises:` section when the function intentionally raises exceptions.
6. `Examples:` section when the function is complex, business-critical, or commonly reused.

Template:

```python
def function_name(param: str, *, option: bool = False) -> int:
    """Short summary of what the function does.

    Longer explanation if needed. Include business assumptions, edge cases,
    and important behavior that a caller should understand.

    Args:
        param: Description of the required input.
        option: Description of the optional behavior and default.

    Returns:
        Description of the returned value.

    Raises:
        ValueError: Explanation of when this is raised.

    Examples:
        >>> function_name("abc", option=True)
        3
    """
    ...
```

---

### 7.2 Docstrings should explain business meaning, not restate code

Weak docstring:

```python
def calculate_roas(revenue: float, spend: float) -> float:
    """Divides revenue by spend."""
    ...
```

Better docstring:

```python
def calculate_roas(revenue: float, spend: float) -> float:
    """Calculate return on ad spend using attributed revenue and media spend.

    Returns 0.0 when spend is zero to avoid division errors in reporting
    pipelines. This convention should be used only for dashboard display;
    finance-grade analysis may require explicit missing-value handling.
    """
    ...
```

The better version explains the reporting convention and its limitation.

---

### 7.3 Worked example: fully documented complex function

```python
from datetime import date
from decimal import Decimal


def calculate_campaign_performance_summary(
    rows: list[dict[str, object]],
    *,
    start_date: date,
    end_date: date,
    attribution_window_days: int,
    include_view_through: bool = False,
    minimum_spend: Decimal = Decimal("0.00"),
) -> dict[str, Decimal]:
    """Calculate paid campaign performance metrics for a reporting window.

    The function aggregates campaign-level rows into a single summary used by
    weekly marketing performance dashboards. Rows outside the reporting window
    are ignored. Rows with spend below `minimum_spend` are excluded before
    metric calculation so that test campaigns and accidental imports do not
    distort blended KPIs.

    Revenue should already be attributed before this function is called. This
    function does not perform attribution matching; it only respects the
    `attribution_window_days` value for auditability and downstream reporting
    metadata.

    Args:
        rows: Campaign performance records. Each record must contain `date`,
            `spend`, `clicks`, `impressions`, `conversions`, `revenue`, and
            `is_view_through` fields.
        start_date: Inclusive start date for the reporting window.
        end_date: Inclusive end date for the reporting window.
        attribution_window_days: Attribution window used by the upstream
            attribution process. Must be greater than zero.
        include_view_through: Whether view-through conversions and revenue are
            included in the returned summary. Defaults to False.
        minimum_spend: Minimum campaign spend required for a row to be included
            in the summary. Defaults to Decimal("0.00").

    Returns:
        A dictionary containing total spend, total revenue, total conversions,
        ROAS, CPA, CPC, CPM, and conversion rate. Monetary values are returned
        as Decimal values rounded by the caller's presentation layer.

    Raises:
        ValueError: If `start_date` is after `end_date`.
        ValueError: If `attribution_window_days` is less than 1.
        KeyError: If a required field is missing from any row.

    Examples:
        >>> rows = [
        ...     {
        ...         "date": date(2026, 5, 1),
        ...         "spend": Decimal("100.00"),
        ...         "clicks": 50,
        ...         "impressions": 1000,
        ...         "conversions": 5,
        ...         "revenue": Decimal("500.00"),
        ...         "is_view_through": False,
        ...     }
        ... ]
        >>> summary = calculate_campaign_performance_summary(
        ...     rows,
        ...     start_date=date(2026, 5, 1),
        ...     end_date=date(2026, 5, 7),
        ...     attribution_window_days=30,
        ... )
        >>> summary["roas"]
        Decimal('5.00')
    """
    if start_date > end_date:
        raise ValueError("start_date must be on or before end_date")

    if attribution_window_days < 1:
        raise ValueError("attribution_window_days must be greater than zero")

    required_fields = {
        "date",
        "spend",
        "clicks",
        "impressions",
        "conversions",
        "revenue",
        "is_view_through",
    }

    filtered_rows = []
    for row in rows:
        missing_fields = required_fields - row.keys()
        if missing_fields:
            raise KeyError(f"Missing required fields: {sorted(missing_fields)}")

        row_date = row["date"]
        if not start_date <= row_date <= end_date:
            continue

        if row["spend"] < minimum_spend:
            continue

        if row["is_view_through"] and not include_view_through:
            continue

        filtered_rows.append(row)

    total_spend = sum(row["spend"] for row in filtered_rows)
    total_revenue = sum(row["revenue"] for row in filtered_rows)
    total_clicks = sum(row["clicks"] for row in filtered_rows)
    total_impressions = sum(row["impressions"] for row in filtered_rows)
    total_conversions = sum(row["conversions"] for row in filtered_rows)

    return {
        "spend": total_spend,
        "revenue": total_revenue,
        "conversions": Decimal(total_conversions),
        "roas": Decimal("0.00") if total_spend == 0 else total_revenue / total_spend,
        "cpa": Decimal("0.00") if total_conversions == 0 else total_spend / total_conversions,
        "cpc": Decimal("0.00") if total_clicks == 0 else total_spend / total_clicks,
        "cpm": Decimal("0.00") if total_impressions == 0 else total_spend / total_impressions * 1000,
        "conversion_rate": Decimal("0.00") if total_clicks == 0 else Decimal(total_conversions) / total_clicks,
    }
```

This example demonstrates several team standards: verb-first naming, typed parameters, keyword-only business rules, safe defaults, explicit validation, readable filtering logic, and a docstring that explains the function’s business role.

---

## 8. Comprehension Policy

Comprehensions can make Python code concise and readable when used for simple transformations and filters. They become harmful when they hide complex business logic, side effects, or deeply nested control flow.

---

### 8.1 Use comprehensions for simple transformations

Good use:

```python
campaign_ids = [campaign["id"] for campaign in campaigns]
```

This is readable because it performs one simple transformation.

---

### 8.2 Use comprehensions for simple filters

Good use:

```python
paid_campaigns = [
    campaign
    for campaign in campaigns
    if campaign["channel"] == "paid_search"
]
```

This is acceptable because the filter condition is direct and easy to understand.

---

### 8.3 Use comprehensions for simple dictionary construction

Good use:

```python
spend_by_campaign = {
    row["campaign_id"]: row["spend"]
    for row in campaign_rows
}
```

This is clear when each key maps directly to one value.

---

### 8.4 Avoid deeply nested comprehensions

Avoid:

```python
values = [
    item["value"]
    for group in groups
    for campaign in group["campaigns"]
    for item in campaign["metrics"]
    if item["name"] in allowed_metrics and item["value"] is not None
]
```

This may be valid Python, but it is difficult to review. Prefer explicit loops when nested data structures or multiple conditions are involved.

Better:

```python
values = []
for group in groups:
    for campaign in group["campaigns"]:
        for item in campaign["metrics"]:
            is_allowed_metric = item["name"] in allowed_metrics
            has_value = item["value"] is not None
            if is_allowed_metric and has_value:
                values.append(item["value"])
```

The explicit version gives names to the conditions, making business logic easier to review.

---

### 8.5 Avoid comprehensions with multi-line business conditions

Avoid:

```python
eligible_rows = [
    row
    for row in rows
    if row["spend"] > 0
    and row["conversions"] > 0
    and row["channel"] in paid_channels
    and row["date"] >= start_date
    and row["date"] <= end_date
    and not row["is_test_campaign"]
]
```

Better:

```python
def is_eligible_performance_row(
    row: dict[str, object],
    *,
    start_date: date,
    end_date: date,
    paid_channels: set[str],
) -> bool:
    return (
        row["spend"] > 0
        and row["conversions"] > 0
        and row["channel"] in paid_channels
        and start_date <= row["date"] <= end_date
        and not row["is_test_campaign"]
    )


eligible_rows = [
    row
    for row in rows
    if is_eligible_performance_row(
        row,
        start_date=start_date,
        end_date=end_date,
        paid_channels=paid_channels,
    )
]
```

The named predicate can be tested independently and reused.

---

### 8.6 Never use comprehensions for side effects

Incorrect:

```python
[send_alert(campaign) for campaign in campaigns if campaign["over_budget"]]
```

Comprehensions should create new collections. They should not be used to perform actions.

Correct:

```python
for campaign in campaigns:
    if campaign["over_budget"]:
        send_alert(campaign)
```

---

### 8.7 Comprehension review rule

A comprehension is acceptable when a reviewer can understand it in one pass. If a reviewer has to mentally simulate several branches, nested loops, or side effects, use a named function or explicit loop instead.

---

## 9. Lambda Policy

Lambda expressions are allowed, but they should be used narrowly. A lambda is an anonymous function. Because it has no name and no docstring, it is a poor place to hide business logic.

---

### 9.1 Use lambdas for simple sort keys

Good use:

```python
campaigns = sorted(campaigns, key=lambda campaign: campaign["spend"])
```

This is acceptable because the lambda is short, local, and obvious.

---

### 9.2 Use lambdas for simple single-use predicates

Acceptable:

```python
high_spend_campaigns = filter(lambda row: row["spend"] > 1000, rows)
```

However, a list comprehension is often more readable:

```python
high_spend_campaigns = [row for row in rows if row["spend"] > 1000]
```

Prefer comprehensions over `filter()` plus lambda when the result is a list.

---

### 9.3 Replace lambdas with named functions when logic has business meaning

Avoid:

```python
rows = filter(
    lambda row: row["medium"] in {"cpc", "paid_social"} and row["spend"] > 0,
    rows,
)
```

Better:

```python
def is_paid_media_row(row: dict[str, object]) -> bool:
    return row["medium"] in {"cpc", "paid_social"} and row["spend"] > 0


paid_rows = [row for row in rows if is_paid_media_row(row)]
```

The named function reveals the business concept and can be tested.

---

### 9.4 Do not assign lambdas to variable names

Avoid:

```python
calculate_roas = lambda revenue, spend: revenue / spend if spend else 0.0
```

Use a normal function:

```python
def calculate_roas(revenue: float, spend: float) -> float:
    return revenue / spend if spend else 0.0
```

Assigning a lambda to a name combines the disadvantages of both approaches: it is named, but still lacks a proper docstring, annotations are awkward, and debugging output is less useful.

---

### 9.5 Lambda review rule

A lambda is acceptable only when it is short, local, obvious, and not business-critical. If it needs a comment, it should probably be a named function.

---

## 10. Error Handling and Validation Standards

Although this document focuses on function design, error handling is part of a good function contract.

### 10.1 Validate inputs at system boundaries

Functions that receive data from APIs, CSV files, spreadsheets, user input, or external services should validate required fields and expected types before performing business calculations.

```python
def validate_campaign_row(row: dict[str, object]) -> None:
    required_fields = {"campaign_id", "date", "spend", "revenue"}
    missing_fields = required_fields - row.keys()
    if missing_fields:
        raise KeyError(f"Missing campaign fields: {sorted(missing_fields)}")
```

### 10.2 Raise specific exceptions

Use specific built-in exceptions such as `ValueError`, `TypeError`, `KeyError`, or custom exceptions when appropriate. Avoid generic `Exception` unless there is a compelling reason.

Weak:

```python
raise Exception("bad date")
```

Better:

```python
raise ValueError("start_date must be on or before end_date")
```

### 10.3 Do not silently swallow errors

Avoid:

```python
try:
    return revenue / spend
except Exception:
    return 0
```

This hides unexpected errors. Handle only the error you expect.

Better:

```python
def calculate_roas(revenue: float, spend: float) -> float:
    if spend == 0:
        return 0.0
    return revenue / spend
```

---

## 11. Function Size and Complexity Standards

There is no strict line limit, but long functions require scrutiny. A function longer than approximately 40 lines should usually be reviewed for possible extraction. A function with several nested branches should be simplified unless the complexity is unavoidable and well documented.

A function may be too complex when:

- It has more than one primary responsibility.
- It mixes data loading, transformation, calculation, and output.
- It contains deeply nested `if` or `for` blocks.
- It has many flags that change behavior.
- It requires extensive comments to explain the control flow.
- It is difficult to unit test without large fixtures.

Refactor by extracting:

- Validation functions.
- Predicate functions such as `is_paid_media_row`.
- Calculation functions such as `calculate_cpa`.
- Formatting functions such as `format_percentage`.
- Data access functions such as `load_platform_spend`.

---

## 12. Examples of Preferred Function Design

### 12.1 Metric calculation function

```python
def calculate_cpa(spend: float, conversions: int) -> float:
    """Calculate cost per acquisition for paid marketing reporting.

    Returns 0.0 when conversions are zero so dashboard calculations do not
    fail. Analysts should treat a zero-conversion CPA as a display convention,
    not as a true economic value.

    Args:
        spend: Total media spend.
        conversions: Number of attributed conversions.

    Returns:
        Cost per acquisition.
    """
    if conversions == 0:
        return 0.0
    return spend / conversions
```

### 12.2 Predicate function

```python
def is_brand_campaign(campaign_name: str, brand_terms: set[str]) -> bool:
    """Return whether a campaign name contains a known brand term."""
    normalized_name = campaign_name.casefold()
    return any(term.casefold() in normalized_name for term in brand_terms)
```

### 12.3 Transformation function

```python
def normalize_utm_medium(medium: str) -> str:
    """Normalize UTM medium values into team-approved reporting categories."""
    normalized_medium = medium.strip().casefold()
    medium_mapping = {
        "cpc": "paid_search",
        "ppc": "paid_search",
        "paid-social": "paid_social",
        "paid_social": "paid_social",
        "email": "email",
    }
    return medium_mapping.get(normalized_medium, "other")
```

### 12.4 Orchestration function

```python
def build_weekly_channel_summary(
    rows: list[dict[str, object]],
    *,
    start_date: date,
    end_date: date,
) -> list[dict[str, object]]:
    """Build weekly marketing channel summary rows for dashboard ingestion."""
    validate_reporting_window(start_date, end_date)
    eligible_rows = filter_reporting_rows(rows, start_date=start_date, end_date=end_date)
    grouped_rows = group_rows_by_channel(eligible_rows)
    return [calculate_channel_summary(channel, rows) for channel, rows in grouped_rows.items()]
```

This orchestration function is acceptable because it coordinates named steps rather than hiding all logic inline.

---

## 13. Anti-Patterns to Avoid

### 13.1 The vague utility function

Avoid functions like:

```python
def process_data(data):
    ...
```

This name says almost nothing. Use a name that describes the specific transformation.

Better:

```python
def remove_test_campaign_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ...
```

### 13.2 The flag-driven mega-function

Avoid:

```python
def generate_report(data, include_email=False, save_csv=False, make_chart=False):
    ...
```

Several flags often mean the function has several responsibilities. Split into named functions.

### 13.3 Hidden global dependencies

Avoid:

```python
ATTRIBUTION_WINDOW = 30


def calculate_revenue(conversions):
    return run_attribution(conversions, ATTRIBUTION_WINDOW)
```

Better:

```python
def calculate_revenue(conversions: list[dict], *, attribution_window_days: int) -> float:
    return run_attribution(conversions, attribution_window_days)
```

Passing the business rule explicitly makes the function easier to test and review.

### 13.4 Mixed return types

Avoid:

```python
def find_campaign(campaign_id: str):
    if campaign_exists(campaign_id):
        return {"id": campaign_id}
    return False
```

Better:

```python
def find_campaign(campaign_id: str) -> dict[str, object] | None:
    if campaign_exists(campaign_id):
        return {"id": campaign_id}
    return None
```

A function should have a predictable return type.

---

## 14. Testing Expectations for Functions

Every public function that contains business logic should have unit tests. The tests should cover normal cases, edge cases, and invalid inputs.

Recommended test categories:

- Standard valid input.
- Empty input.
- Missing required fields.
- Zero denominators for metric calculations.
- Boundary dates.
- Unknown campaign channels.
- Null or missing optional values.
- Case and whitespace variations in text normalization.
- Duplicate records when relevant.
- Business-rule exceptions.

Example test cases for `calculate_roas`:

```python
def test_calculate_roas_returns_revenue_divided_by_spend():
    assert calculate_roas(500.0, 100.0) == 5.0


def test_calculate_roas_returns_zero_when_spend_is_zero():
    assert calculate_roas(500.0, 0.0) == 0.0
```

---

## 15. 12-Question Function-Level Code Review Checklist

Use this checklist during pull request review when evaluating new or changed functions.

1. **Name clarity:** Does the function name use `snake_case`, start with a useful verb, and clearly describe the business or technical action?
2. **Single responsibility:** Does the function do one coherent job, or is it combining loading, cleaning, calculation, formatting, and output?
3. **Signature clarity:** Are required inputs positional only when obvious, and are configuration or business-rule values keyword-only?
4. **Default safety:** Are default values safe, intentional, documented, and aligned with team-approved business rules?
5. **Mutable defaults:** Does the function avoid mutable default arguments such as `[]`, `{}`, or `set()`?
6. **Type hints:** Are all public parameters and return values annotated with useful type hints?
7. **Nullable values:** Are `None` values represented clearly with `| None`, and does the function handle them explicitly?
8. **Docstring quality:** Does the docstring explain purpose, arguments, return value, raised exceptions, and business assumptions where needed?
9. **Comprehension readability:** Are comprehensions simple and readable, avoiding deep nesting, side effects, and complex multi-line conditions?
10. **Lambda appropriateness:** Are lambdas limited to short, local, obvious expressions such as sort keys or simple predicates?
11. **Error handling:** Does the function validate boundary inputs and raise specific exceptions rather than silently swallowing errors?
12. **Testability:** Can the function be unit tested with small, controlled inputs without depending on global state, live APIs, current time, or hidden side effects?

A function does not need to be perfect to pass review, but every checklist concern should be consciously addressed. Review comments should reference this checklist when requesting changes.

---

## 16. Team Adoption Rules

The team will apply this standard as follows:

1. New production functions must follow this document.
2. Existing functions should be improved when they are touched for feature work or bug fixes.
3. Pull requests should use the 12-question checklist for function-level review.
4. Shared utilities should be held to the strictest version of the standard.
5. Notebook logic should be refactored into standard-compliant functions before being scheduled, reused, or merged into production workflows.
6. Business-rule functions should include docstrings and tests even when they are short.

This standard is intended to improve consistency, not slow delivery. Small private helpers can remain lightweight, but public and business-critical functions must be explicit, typed, documented, and reviewable.

---

## 17. Appendix A: Quick Reference

### Naming

- Use `snake_case`.
- Prefer verb-first names.
- Avoid vague names like `process_data` or `handle_stuff`.
- Use business concepts in function names.

### Signatures

- Use positional arguments for obvious required inputs.
- Use keyword-only arguments for configuration and business rules.
- Avoid unsafe defaults.
- Never use mutable defaults.
- Avoid `*args` and `**kwargs` unless there is a clear design reason.

### Type hints

- Required for public functions.
- Optional only for trivial private helpers.
- Prefer `list[T]`, `dict[K, V]`, and `str | None`.
- Avoid broad `Any` and overly flexible unions.

### Docstrings

- Use Google style.
- Explain business meaning and edge cases.
- Include `Args`, `Returns`, `Raises`, and `Examples` when useful.

### Comprehensions

- Use for simple transformations and filters.
- Avoid nested and side-effect comprehensions.
- Extract named predicates for complex conditions.

### Lambdas

- Use for simple sort keys and local one-line predicates.
- Do not assign lambdas to names.
- Do not hide business rules in lambdas.

---

## 18. Appendix B: Standard Function Template

```python
def calculate_metric_name(
    required_value: float,
    *,
    business_rule: int,
    include_adjustment: bool = False,
) -> float:
    """Calculate a specific marketing metric for a defined reporting purpose.

    Explain the business rule, the reporting convention, and any important
    edge-case behavior here.

    Args:
        required_value: Description of the main required input.
        business_rule: Description of the explicit business-rule parameter.
        include_adjustment: Whether to include the optional adjustment.
            Defaults to False.

    Returns:
        The calculated metric value.

    Raises:
        ValueError: If the business rule value is invalid.
    """
    if business_rule < 1:
        raise ValueError("business_rule must be greater than zero")

    if include_adjustment:
        return required_value * business_rule

    return required_value
```

---

## 19. Final Standard Statement

A good Python function for the marketing analytics team is explicit, focused, typed, documented, and testable. It should communicate business intent through its name, protect correctness through its signature, and make review straightforward through clear structure. Cleverness is not the goal. Reliable analytics delivery is the goal.
