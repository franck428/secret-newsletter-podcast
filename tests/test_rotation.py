from __future__ import annotations

import json
from pathlib import Path

from src.build_episode import build_episode, save_episode_and_state
from src.newsletter import validate_newsletter
from tests.test_newsletter import payload


def test_episode_selects_five_products(tmp_path: Path) -> None:
    state = tmp_path / "state.json"
    episode_file = tmp_path / "episode.json"
    newsletter = validate_newsletter(payload())
    episode = build_episode(newsletter, state, "2026-08-18")
    assert len(episode["products"]) == 5
    assert episode["title"] == "Five Finds That Are Genuinely Worth a Look"


def test_dialogue_never_claims_physical_testing(tmp_path: Path) -> None:
    episode = build_episode(validate_newsletter(payload()), tmp_path / "missing.json")
    transcript = " ".join(x["text"] for x in episode["segments"]).lower()
    assert "not physically tested" in transcript
    assert "$9.99/month" not in transcript
    assert "four dollars and ninety-nine cents" in transcript
    assert "i managed to buy" not in transcript
