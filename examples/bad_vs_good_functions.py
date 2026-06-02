"""Bad vs. good examples for function design review."""

# -----------------------------------------------------------------------------
# Example 1: Metric calculation
# -----------------------------------------------------------------------------

# Weak: unclear names, no type hints, no edge-case handling.
def roas(r, s):
    return r / s


# Better: clear name, type hints, edge-case behavior, and business meaning.
def calculate_roas(revenue: float, spend: float) -> float | None:
    """Calculate return on ad spend, returning None when spend is zero."""
    if spend == 0:
        return None
    return revenue / spend


# -----------------------------------------------------------------------------
# Example 2: Lambda vs. named function
# -----------------------------------------------------------------------------

campaigns = [
    {"name": "Brand Search", "spend": 1200.0, "revenue": 5400.0},
    {"name": "Retargeting", "spend": 800.0, "revenue": 1600.0},
]

# Acceptable lambda: short, local, obvious sort key.
sorted_by_spend = sorted(campaigns, key=lambda campaign: campaign["spend"])


# Better named function when the logic has business meaning.
def calculate_campaign_efficiency_score(campaign: dict[str, float | str]) -> float:
    """Calculate a simple efficiency score for campaign ranking."""
    spend = float(campaign["spend"])
    revenue = float(campaign["revenue"])
    if spend == 0:
        return 0.0
    return revenue / spend


sorted_by_efficiency = sorted(campaigns, key=calculate_campaign_efficiency_score, reverse=True)


# -----------------------------------------------------------------------------
# Example 3: Comprehension readability
# -----------------------------------------------------------------------------

raw_campaign_names = ["  Brand Search ", "PAID SOCIAL", "", " Retargeting  "]

# Good comprehension: simple transformation and filter.
normalized_names = [
    name.strip().lower()
    for name in raw_campaign_names
    if name.strip()
]

# Avoid deeply nested comprehension when the logic becomes business-heavy.
def normalize_non_empty_campaign_names(names: list[str]) -> list[str]:
    """Return non-empty campaign names with consistent casing and spacing."""
    normalized = []

    for name in names:
        cleaned_name = " ".join(name.strip().lower().split())
        if cleaned_name:
            normalized.append(cleaned_name)

    return normalized
