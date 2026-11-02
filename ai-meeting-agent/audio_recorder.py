import argparse
import sys
import time
from pathlib import Path

import sounddevice as sd
import soundfile as sf


def record(output_path: Path, duration: float | None = None) -> None:
    sample_rate = 44_100
    block_size = 1_024
    frames = []
    started_at = time.monotonic()

    print("Recording... Press Ctrl+C to stop.")
    try:
        with sd.InputStream(
            samplerate=sample_rate,
            channels=1,
            dtype="int16",
            blocksize=block_size,
        ) as stream:
            while duration is None or time.monotonic() - started_at < duration:
                audio, overflowed = stream.read(block_size)
                frames.append(audio.copy())
                if overflowed:
                    print("Warning: audio input overflowed.", file=sys.stderr)
    except KeyboardInterrupt:
        print("\nRecording stopped.")

    if not frames:
        raise RuntimeError("No audio was recorded.")

    import numpy as np

    recording = np.concatenate(frames, axis=0)
    sf.write(output_path, recording, sample_rate)
    print(f"Saved {len(recording) / sample_rate:.1f} seconds to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Record microphone audio to a WAV file.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("recording.wav"),
        help="Output WAV path (default: recording.wav)",
    )
    parser.add_argument(
        "-d",
        "--duration",
        type=float,
        help="Recording duration in seconds (default: record until Ctrl+C)",
    )
    args = parser.parse_args()

    if args.duration is not None and args.duration <= 0:
        parser.error("--duration must be greater than zero")

    record(args.output, args.duration)


if __name__ == "__main__":
    main()
