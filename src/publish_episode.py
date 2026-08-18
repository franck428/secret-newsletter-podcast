from __future__ import annotations

import html
import json
import shutil
from pathlib import Path


def publish(episode_path: Path, mp3_path: Path, public_dir: Path) -> None:
    episode = json.loads(episode_path.read_text(encoding="utf-8"))
    public_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(mp3_path, public_dir / "latest-podcast.mp3")
    metadata = {
        "episode_id": episode["episode_id"],
        "date": episode["date"],
        "title": episode["title"],
        "edition_id": episode["edition_id"],
        "products": [{"name": p["name"], "url": p["url"], "price": p["price"]} for p in episode["products"]],
        "audio_url": "latest-podcast.mp3",
    }
    (public_dir / "latest.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    title = html.escape(episode["title"])
    links = "".join(f'<li><a href="{html.escape(p["url"], quote=True)}">{html.escape(p["name"])}</a> — {html.escape(p["price"])}</li>' for p in episode["products"])
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>body{{font-family:system-ui;max-width:720px;margin:48px auto;padding:0 20px;color:#0f172a}}audio{{width:100%}}a{{color:#2563eb}}</style></head>
<body><h1>The Secret Newsletter Podcast</h1><h2>{title}</h2><audio controls preload="metadata" src="latest-podcast.mp3"></audio>
<h3>Today’s five finds</h3><ol>{links}</ol>
<p>30-day free trial, then $4.99/month, cancel anytime.</p></body></html>"""
    (public_dir / "index.html").write_text(page, encoding="utf-8")
    (public_dir / ".nojekyll").touch()
