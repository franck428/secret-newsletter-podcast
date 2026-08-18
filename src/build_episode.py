from __future__ import annotations

import json
from dataclasses import asdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from .newsletter import Newsletter, Product


def _load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def select_product(newsletter: Newsletter, episode_date: str) -> tuple[int, Product, int]:
    """Select deterministically because every Actions runner starts with no local state."""
    edition_day = datetime.fromisoformat(
        newsletter.edition_date.replace("Z", "+00:00")
    ).astimezone(timezone.utc).date()
    current_day = date.fromisoformat(episode_date)
    elapsed_days = max(0, (current_day - edition_day).days)
    index = elapsed_days % len(newsletter.products)
    angle_cycle = elapsed_days // len(newsletter.products)
    return index, newsletter.products[index], angle_cycle


def build_dialogue(products: tuple[Product, ...]) -> list[dict[str, str]]:
    lines = [
        {"speaker": "Maya", "text": "Today we are doing something different. We went through all ten finds in the latest approved edition and chose the five that created the strongest combination of surprise, everyday usefulness, and price."},
        {"speaker": "Daniel", "text": "And this is a serious shortlist. We are not trying to praise every gadget. The question is simple: does it solve a real problem, and does the price make you look twice?"},
        {"speaker": "Maya", "text": "Exactly. We have not physically tested these products, so we will stick to the approved information and tell you what deserves a closer look. Let us start with number five."},
    ]
    for position, product in enumerate(reversed(products), start=1):
        rank = 6 - position
        lines.extend([
            {"speaker": "Daniel", "text": f"At number {rank}: {product.name}. {product.description} The editorial reason is simple: {product.why_it_made_the_list}"},
            {"speaker": "Maya", "text": "What makes that interesting in real life is the reduction in friction. This is not technology for a specification sheet. It can make a repeated task faster, calmer, or simply less annoying."},
            {"speaker": "Daniel", "text": f"And the approved price for this edition is {product.price}. That is where curiosity becomes a serious value discussion. Check compatibility, the live price, and availability on the full product page before deciding."},
        ])
    lines.extend([
        {"speaker": "Daniel", "text": "That is especially true with marketplace finds. Some eBay listings are temporary. Availability can change quickly, and a listing that shows only a small quantity may disappear before the next edition. We cannot promise stock, so always check the current OneFantasticShop page."},
        {"speaker": "Maya", "text": "And that is why I think the work behind The Secret Newsletter has value. You are not subscribing to a random product list. The team searches, filters, checks the details, and keeps only ten discoveries—the ten that made them stop."},
        {"speaker": "Maya", "text": "If even one of today’s five made you curious, imagine receiving a fresh selection without doing the research yourself. The Secret Newsletter includes a 30-day free trial, then four dollars and ninety-nine cents a month, cancel anytime."},
        {"speaker": "Daniel", "text": "Visit OneFantasticShop dot net for the full product details and the current availability. We find it. We explain it. You decide."},
        {"speaker": "Maya", "text": "And tomorrow, we will be back with another serious look at the discoveries worth your time."},
    ])
    return lines


def build_episode(newsletter: Newsletter, state_path: Path, episode_date: str | None = None) -> dict[str, Any]:
    day = episode_date or date.today().isoformat()
    selected = newsletter.products[:5]
    return {
        "episode_id": f"{newsletter.edition_id}-{day}-top-five",
        "date": day,
        "title": "Five Finds That Are Genuinely Worth a Look",
        "edition_id": newsletter.edition_id,
        "product_index": 0,
        "products": [asdict(product) for product in selected],
        "hosts": {"Maya": "af_heart", "Daniel": "am_michael"},
        "segments": build_dialogue(selected),
    }


def save_episode_and_state(episode: dict[str, Any], episode_path: Path, state_path: Path) -> None:
    episode_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    episode_path.write_text(json.dumps(episode, indent=2) + "\n", encoding="utf-8")
    state = {
        "edition_id": episode["edition_id"],
        "last_product_index": episode["product_index"],
        "last_episode_id": episode["episode_id"],
    }
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
