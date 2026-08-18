from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, urlopen


class NewsletterValidationError(ValueError):
    """Raised when the approved newsletter source is unsafe or incomplete."""


@dataclass(frozen=True)
class Product:
    name: str
    price: str
    description: str
    why_it_made_the_list: str
    url: str
    category: str = ""
    image: str = ""


@dataclass(frozen=True)
class Newsletter:
    edition_id: str
    edition_date: str
    title: str
    updated_at: str
    products: tuple[Product, ...]


def _required_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise NewsletterValidationError(f"Missing or empty field: {field}")
    return value.strip()


def _validate_product_url(value: Any, field: str) -> str:
    url = _required_text(value, field)
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or host not in {
        "onefantasticshop.net",
        "www.onefantasticshop.net",
    }:
        raise NewsletterValidationError(
            f"{field} must be an HTTPS OneFantasticShop.net product URL"
        )
    return url


def validate_newsletter(payload: Any) -> Newsletter:
    if not isinstance(payload, dict):
        raise NewsletterValidationError("Newsletter payload must be a JSON object")

    raw_products = payload.get("products")
    if not isinstance(raw_products, list) or len(raw_products) != 10:
        raise NewsletterValidationError("Approved newsletter must contain exactly 10 products")

    products: list[Product] = []
    seen_urls: set[str] = set()
    for index, raw in enumerate(raw_products):
        prefix = f"products[{index}]"
        if not isinstance(raw, dict):
            raise NewsletterValidationError(f"{prefix} must be an object")
        url = _validate_product_url(raw.get("url"), f"{prefix}.url")
        if url in seen_urls:
            raise NewsletterValidationError(f"Duplicate product URL: {url}")
        seen_urls.add(url)
        products.append(
            Product(
                name=_required_text(raw.get("name"), f"{prefix}.name"),
                price=_required_text(raw.get("price"), f"{prefix}.price"),
                description=_required_text(raw.get("description"), f"{prefix}.description"),
                why_it_made_the_list=_required_text(
                    raw.get("why_it_made_the_list"),
                    f"{prefix}.why_it_made_the_list",
                ),
                url=url,
                category=str(raw.get("category") or "").strip(),
                image=str(raw.get("image") or "").strip(),
            )
        )

    edition_date = _required_text(payload.get("edition_date"), "edition_date")
    updated_at = _required_text(payload.get("updated_at"), "updated_at")
    try:
        datetime.fromisoformat(edition_date.replace("Z", "+00:00"))
        datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise NewsletterValidationError("edition_date and updated_at must be ISO-8601") from exc

    return Newsletter(
        edition_id=_required_text(payload.get("edition_id"), "edition_id"),
        edition_date=edition_date,
        title=_required_text(payload.get("title"), "title"),
        updated_at=updated_at,
        products=tuple(products),
    )


def fetch_latest_newsletter(source: str, timeout: int = 30) -> Newsletter:
    if source.startswith(("http://", "https://")):
        request = Request(source, headers={"User-Agent": "secret-newsletter-podcast/1.0"})
        with urlopen(request, timeout=timeout) as response:
            payload = json.load(response)
    else:
        payload = json.loads(Path(source).read_text(encoding="utf-8"))
    return validate_newsletter(payload)
