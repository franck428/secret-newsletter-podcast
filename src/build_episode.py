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
    recorder, lock, tracker, buddha, speaker = products
    return [
        {"speaker": "Maya", "text": "Welcome to The Secret Newsletter Podcast. I’m Maya."},
        {"speaker": "Daniel", "text": "And I’m Daniel. Every day, we take the ten discoveries from the latest approved Secret Newsletter and argue about the five that are actually worth your attention."},
        {"speaker": "Maya", "text": "The newsletter’s promise is simple: ten things you probably did not know existed, at prices you would not expect. You can find it through OneFantasticShop dot net."},
        {"speaker": "Daniel", "text": "They do the searching. We do the debating. You keep your evening instead of opening forty-seven browser tabs and forgetting why you needed a Bluetooth speaker in the first place."},
        {"speaker": "Maya", "text": "That sounds oddly specific."},
        {"speaker": "Daniel", "text": "I have a tab problem. Let’s move on."},
        {"speaker": "Maya", "text": "Today’s theme is value. Not the fanciest products—the ones where the everyday usefulness feels much bigger than the price. Our five picks start below twenty-three dollars and stay under forty."},
        {"speaker": "Daniel", "text": f"Number five is the {speaker.name}, at {speaker.price}. A phone stand and a Bluetooth speaker in one."},
        {"speaker": "Maya", "text": "At first I thought, fine, two ordinary things sharing a desk. Then I pictured the kitchen. Your phone is upright for a recipe, the sound is loud enough to hear over the fan, and you are not leaning your phone against a bag of flour."},
        {"speaker": "Daniel", "text": "Or using it for video calls, watching something at your desk, or giving a tablet better sound. Twenty-six ninety-nine is the price of a basic stand and a small speaker anyway."},
        {"speaker": "Maya", "text": "Important limitation: it does not charge the phone. So it is a useful desk companion, not a magical piece of furniture."},
        {"speaker": "Daniel", "text": "I was promised magical furniture."},
        {"speaker": "Maya", "text": "You were promised a product newsletter. Manage your expectations."},
        {"speaker": "Daniel", "text": f"Number four: the {buddha.name}, at {buddha.price}. This one surprised me because it solves a problem most apps make worse."},
        {"speaker": "Maya", "text": "Exactly. When you are stressed, the last thing you need is to unlock your phone, see twelve notifications, open a meditation app, reject an upgrade offer, and somehow remain calm."},
        {"speaker": "Daniel", "text": "This is a small visual breathing guide. Color prompts lead you through several breathing patterns, with optional nature sounds. Put it on a desk or nightstand and use it for a short reset."},
        {"speaker": "Maya", "text": "It is not a medical device and it is not a replacement for professional care. But for twenty-five ninety-five, turning ‘remember to breathe’ into a visible routine for adults or kids is a smart piece of design."},
        {"speaker": "Daniel", "text": "Number three is the cheapest pick: the ENGERWALL fitness tracker at twenty-two ninety-nine."},
        {"speaker": "Maya", "text": "Twenty-two ninety-nine. Daniel, that is less than two lunches."},
        {"speaker": "Daniel", "text": "One lunch if you order guacamole."},
        {"speaker": "Maya", "text": "Fair. But steps, sleep, heart rate, workout modes, reminders, phone notifications, water resistance, and several days of battery life? That is the kind of price that makes me check whether I misread the page."},
        {"speaker": "Daniel", "text": "The real value is not collecting numbers. It is noticing patterns. Did you move today? Are you sleeping consistently? Have you been sitting so long that your chair now considers you family?"},
        {"speaker": "Maya", "text": "Again, wellness readings from an inexpensive tracker should not be treated as a medical diagnosis. But as a daily nudge to walk, hydrate, and pay attention, the price-to-utility ratio is excellent."},
        {"speaker": "Daniel", "text": f"Number two: the {lock.name}. The approved price is {lock.price}."},
        {"speaker": "Maya", "text": "This might be the strongest practical bargain. Fingerprint, passcode, app, key fob, and a traditional key. The point is not to make your door look futuristic. It is to stop hiding a spare key under a flowerpot like every burglar has never heard of flowerpots."},
        {"speaker": "Daniel", "text": "You can give family members their own access, avoid copying keys, and use different entry methods. The product page says it fits many standard American doors and installs with a screwdriver, but measurements and compatibility need to be checked first."},
        {"speaker": "Maya", "text": "Thirty-eight dollars for an everyday security and convenience upgrade is exactly the reaction this newsletter is built around: I did not expect that product to cost that little."},
        {"speaker": "Daniel", "text": f"And number one: the {recorder.name}, at {recorder.price}."},
        {"speaker": "Maya", "text": "This is the one I would use most. Record a meeting, lecture, interview, or an idea while walking. The device is designed to transcribe and summarize the audio, with multilingual support and internal storage."},
        {"speaker": "Daniel", "text": "The daily value is time. If a one-hour meeting creates another hour of replaying audio and typing notes, a thirty-nine ninety-five recorder that helps organize the material has a very clear economic argument."},
        {"speaker": "Maya", "text": "And no, we have not physically tested its transcription accuracy. Check the app terms, language support, privacy details, and current specifications. But as a concept at under forty dollars, this is the product that made both of us stop."},
        {"speaker": "Daniel", "text": "So our five prices are twenty-two ninety-nine, twenty-five ninety-five, twenty-six ninety-nine, thirty-eight dollars, and thirty-nine ninety-five. That is a remarkably affordable shortlist."},
        {"speaker": "Maya", "text": "And this is why The Secret Newsletter is more interesting than a page of discounts. A discount on something boring is still boring. The useful work is discovering products you would never have searched for, then explaining why they might matter."},
        {"speaker": "Daniel", "text": "Some marketplace finds, including eBay listings, can be temporary. Availability and prices can change, especially when a seller has only a small quantity. We will never invent a stock number, so check the live OneFantasticShop page when something interests you."},
        {"speaker": "Maya", "text": "The team at OneFantasticShop keeps searching, filtering, and updating the discoveries. The Secret Newsletter offers a 30-day free trial, then four dollars and ninety-nine cents a month, cancel anytime."},
        {"speaker": "Daniel", "text": "Go to OneFantasticShop dot net for the full details on today’s five products and to find The Secret Newsletter."},
        {"speaker": "Maya", "text": "We find it. We explain it. You decide. I’m Maya."},
        {"speaker": "Daniel", "text": "And I’m Daniel. I’m going to close some browser tabs."},
        {"speaker": "Maya", "text": "Start with the guacamole tab. See you next time."},
    ]


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
        "hosts": {"Maya": "af_bella", "Daniel": "am_puck"},
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
