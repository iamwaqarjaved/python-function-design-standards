"""Reusable marketing analytics metric functions.

These examples demonstrate clear names, explicit signatures, type hints,
Google-style docstrings, and predictable edge-case behavior.
"""


def calculate_roas(revenue: float, spend: float) -> float | None:
    """Calculate return on ad spend.

    Args:
        revenue: Revenue attributed to a campaign, channel, or reporting segment.
        spend: Advertising spend for the same campaign, channel, or segment.

    Returns:
        The revenue-to-spend ratio. Returns None when spend is zero because ROAS
        is undefined without spend.

    Raises:
        ValueError: If revenue or spend is negative.
    """
    if revenue < 0:
        raise ValueError("revenue cannot be negative")
    if spend < 0:
        raise ValueError("spend cannot be negative")
    if spend == 0:
        return None

    return revenue / spend


def calculate_ctr(clicks: int, impressions: int) -> float | None:
    """Calculate click-through rate.

    Args:
        clicks: Number of ad clicks.
        impressions: Number of ad impressions.

    Returns:
        Clicks divided by impressions. Returns None when impressions is zero.

    Raises:
        ValueError: If clicks or impressions is negative, or clicks exceed impressions.
    """
    if clicks < 0:
        raise ValueError("clicks cannot be negative")
    if impressions < 0:
        raise ValueError("impressions cannot be negative")
    if clicks > impressions:
        raise ValueError("clicks cannot exceed impressions")
    if impressions == 0:
        return None

    return clicks / impressions


def normalize_campaign_name(name: str) -> str:
    """Normalize a campaign name for consistent matching and grouping.

    Args:
        name: Raw campaign name from an advertising platform, UTM parameter,
            spreadsheet, or reporting export.

    Returns:
        A lowercase campaign name with trimmed whitespace and collapsed spaces.
    """
    return " ".join(name.strip().lower().split())


def classify_paid_channel(source: str, medium: str) -> str:
    """Classify a source and medium pair into a paid marketing channel.

    Args:
        source: UTM source or platform source value.
        medium: UTM medium or campaign medium value.

    Returns:
        A normalized marketing channel label.
    """
    normalized_source = source.strip().lower()
    normalized_medium = medium.strip().lower()

    if normalized_source in {"google", "bing"} and normalized_medium in {"cpc", "paid_search", "ppc"}:
        return "paid_search"

    if normalized_source in {"facebook", "instagram", "meta", "tiktok", "linkedin"}:
        if normalized_medium in {"paid_social", "cpc", "paid"}:
            return "paid_social"

    if normalized_medium in {"display", "banner", "programmatic"}:
        return "display"

    return "other_paid"
