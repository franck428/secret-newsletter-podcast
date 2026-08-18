from __future__ import annotations

import json
from pathlib import Path

from src.build_episode import build_episode, save_episode_and_state
from src.newsletter import validate_newsletter
from tests.test_newsletter import payload


def test_rotation_is_deterministic_and_resets_for_new_edition(tmp_path: Path) -> None:
    state = tmp_path / "state.json"
    episode_file = tmp_path / "episode.json"
    newsletter = validate_newsletter(payload())
    first = build_episode(newsletter, state, "2026-08-18")
    second = build_episode(newsletter, state, "2026-08-19")
    assert (first["product_index"], second["product_index"]) == (0, 1)

    # A fresh runner with no state must make the same choice.
    assert build_episode(newsletter, tmp_path / "absent.json", "2026-08-19")["product_index"] == 1

    changed = payload()
    changed["edition_id"] = "test-edition-2"
    changed["edition_date"] = "2026-08-20T08:00:00Z"
    reset = build_episode(validate_newsletter(changed), state, "2026-08-20")
    assert reset["product_index"] == 0


def test_dialogue_never_claims_physical_testing(tmp_path: Path) -> None:
    episode = build_episode(validate_newsletter(payload()), tmp_path / "missing.json")
    transcript = " ".join(x["text"] for x in episode["segments"]).lower()
    assert "we have not physically tested it" in transcript
    assert "$9.99/month" not in transcript
    assert "four dollars and ninety-nine cents" in transcript
