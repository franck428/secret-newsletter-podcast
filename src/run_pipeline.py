from __future__ import annotations

import argparse
from pathlib import Path

from .build_episode import build_episode, save_episode_and_state
from .newsletter import fetch_latest_newsletter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Permanent latest newsletter JSON URL or local file")
    parser.add_argument("--episode-date")
    parser.add_argument("--skip-audio", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    episode_path = root / "data/current_episode.json"
    state_path = root / "data/rotation_state.json"
    public_dir = root / "public"
    newsletter = fetch_latest_newsletter(args.source)
    episode = build_episode(newsletter, state_path, args.episode_date)
    save_episode_and_state(episode, episode_path, state_path)
    if not args.skip_audio:
        from .generate_audio import generate_audio
        from .publish_episode import publish

        mp3_path = root / "build/latest-podcast.mp3"
        generate_audio(episode_path, mp3_path, root / "build/audio")
        publish(episode_path, mp3_path, public_dir)


if __name__ == "__main__":
    main()
