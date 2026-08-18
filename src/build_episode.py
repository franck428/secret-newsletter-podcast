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


def build_dialogue(product: Product, angle_cycle: int = 0) -> list[dict[str, str]]:
    angle_lines = (
        "The useful question is not whether it has the longest feature list. It is whether it solves a real, everyday problem without making things complicated.",
        "Today, let us look at the value equation: what friction could this remove, and is that convenience worth the current price?",
        "This time, the interesting angle is who it is actually for. A surprising product can be clever and still not belong in every home.",
    )
    angle_line = angle_lines[angle_cycle % len(angle_lines)]
    if product.price.lower().startswith("see current"):
        price_line = "The current price is shown on the product page. Check it before deciding, because prices can change."
    else:
        price_line = f"The approved price in the current edition is {product.price}. Prices can change, so check the current product page before deciding."
    return [
        {"speaker": "Maya", "text": "Quick question: when was the last time a product made you stop and say, wait, that exists?"},
        {"speaker": "Daniel", "text": f"That is exactly what happened with {product.name}. It sounds unusual, but the idea is surprisingly straightforward."},
        {"speaker": "Maya", "text": product.description},
        {"speaker": "Daniel", "text": f"And this is why it made the list: {product.why_it_made_the_list}"},
        {"speaker": "Maya", "text": angle_line},
        {"speaker": "Daniel", "text": price_line},
        {"speaker": "Maya", "text": "I can see this making sense for someone who values a simple tool with an immediate purpose, especially when the alternative is slower, messier, or more expensive."},
        {"speaker": "Daniel", "text": "We have not physically tested it, so take a close look at the specifications and confirm that it fits your situation."},
        {"speaker": "Maya", "text": "You will find the full product details through OneFantasticShop.net."},
        {"speaker": "Daniel", "text": "And if you enjoy discovering things you did not know existed, The Secret Newsletter gives you ten carefully selected finds."},
        {"speaker": "Maya", "text": "It comes with a 30-day free trial, then four dollars and ninety-nine cents a month, cancel anytime."},
        {"speaker": "Daniel", "text": "We find it. We explain it. You decide. See you tomorrow."},
    ]


def build_episode(newsletter: Newsletter, state_path: Path, episode_date: str | None = None) -> dict[str, Any]:
    day = episode_date or date.today().isoformat()
    index, product, angle_cycle = select_product(newsletter, day)
    return {
        "episode_id": f"{newsletter.edition_id}-{day}-{index + 1}",
        "date": day,
        "title": f"The Find of the Day: {product.name}",
        "edition_id": newsletter.edition_id,
        "product_index": index,
        "angle_cycle": angle_cycle,
        "product": asdict(product),
        "hosts": {"Maya": "af_heart", "Daniel": "am_michael"},
        "segments": build_dialogue(product, angle_cycle),
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
