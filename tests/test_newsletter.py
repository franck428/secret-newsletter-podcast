from __future__ import annotations

from copy import deepcopy

import pytest

from src.newsletter import NewsletterValidationError, validate_newsletter


def payload() -> dict:
    return {
        "edition_id": "test-edition-1",
        "edition_date": "2026-08-18T08:00:00Z",
        "updated_at": "2026-08-18T08:10:00Z",
        "title": "Test edition",
        "products": [
            {
                "name": f"Test product {i}",
                "price": "$9.99",
                "description": "Test-only description.",
                "why_it_made_the_list": "Test-only reason.",
                "url": f"https://onefantasticshop.net/test-product-{i}",
            }
            for i in range(10)
        ],
    }


def test_accepts_exactly_ten_valid_products() -> None:
    newsletter = validate_newsletter(payload())
    assert len(newsletter.products) == 10


def test_rejects_non_ofs_product_url() -> None:
    value = payload()
    value["products"][0]["url"] = "https://amazon.com/example"
    with pytest.raises(NewsletterValidationError, match="OneFantasticShop.net"):
        validate_newsletter(value)


def test_rejects_missing_product() -> None:
    value = payload()
    value["products"].pop()
    with pytest.raises(NewsletterValidationError, match="exactly 10"):
        validate_newsletter(value)


def test_rejects_duplicate_urls() -> None:
    value = deepcopy(payload())
    value["products"][1]["url"] = value["products"][0]["url"]
    with pytest.raises(NewsletterValidationError, match="Duplicate"):
        validate_newsletter(value)

