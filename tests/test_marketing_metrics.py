import pytest

from examples.marketing_metrics import calculate_ctr, calculate_roas, normalize_campaign_name


def test_calculate_roas_returns_ratio() -> None:
    assert calculate_roas(revenue=5000.0, spend=1000.0) == 5.0


def test_calculate_roas_returns_none_for_zero_spend() -> None:
    assert calculate_roas(revenue=5000.0, spend=0.0) is None


def test_calculate_roas_rejects_negative_spend() -> None:
    with pytest.raises(ValueError):
        calculate_roas(revenue=5000.0, spend=-100.0)


def test_calculate_ctr_returns_ratio() -> None:
    assert calculate_ctr(clicks=25, impressions=1000) == 0.025


def test_calculate_ctr_returns_none_for_zero_impressions() -> None:
    assert calculate_ctr(clicks=0, impressions=0) is None


def test_calculate_ctr_rejects_clicks_above_impressions() -> None:
    with pytest.raises(ValueError):
        calculate_ctr(clicks=101, impressions=100)


def test_normalize_campaign_name() -> None:
    assert normalize_campaign_name("  Brand   Search  ") == "brand search"
