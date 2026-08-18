from __future__ import annotations

import json
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf


SAMPLE_RATE = 24_000


def generate_audio(episode_path: Path, output_mp3: Path, work_dir: Path) -> None:
    from kokoro import KPipeline

    episode = json.loads(episode_path.read_text(encoding="utf-8"))
    pipeline = KPipeline(lang_code="a")
    work_dir.mkdir(parents=True, exist_ok=True)
    pieces: list[np.ndarray] = []
    silence = np.zeros(int(SAMPLE_RATE * 0.22), dtype=np.float32)

    for segment in episode["segments"]:
        voice = episode["hosts"][segment["speaker"]]
        chunks = [audio for _, _, audio in pipeline(segment["text"], voice=voice, speed=1.0)]
        if not chunks:
            raise RuntimeError(f"Kokoro returned no audio for {segment['speaker']}")
        pieces.extend(np.asarray(chunk, dtype=np.float32) for chunk in chunks)
        pieces.append(silence)

    combined = np.concatenate(pieces)
    wav_path = work_dir / "episode.wav"
    sf.write(wav_path, combined, SAMPLE_RATE)
    output_mp3.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error", "-i", str(wav_path),
            "-codec:a", "libmp3lame", "-b:a", "128k", str(output_mp3),
        ],
        check=True,
    )

