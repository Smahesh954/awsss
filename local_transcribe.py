
import sys
from pathlib import Path
from faster_whisper import WhisperModel

folder = Path(__file__).resolve().parent

# Use a supplied audio filename, or default to meeting.wav
audio = Path(sys.argv[1]) if len(sys.argv) > 1 else folder / "meeting.wav"

if not audio.is_absolute():
    audio = folder / audio

if not audio.exists():
    raise FileNotFoundError(f"Audio file not found: {audio}")

print("Loading base model...", flush=True)
model = WhisperModel("base", device="cpu", compute_type="int8")

print(f"Transcribing {audio.name}...", flush=True)
segments, info = model.transcribe(
    str(audio),
    beam_size=5,
    vad_filter=False,
    condition_on_previous_text=False,
    language="en",
)

parts = []
for segment in segments:
    print(
        f"[{segment.start:.1f}s - {segment.end:.1f}s] {segment.text}",
        flush=True
    )
    parts.append(segment.text.strip())

# Keep the original transcript.txt behavior for normal runs.
# Background segments get their own transcript files.
if audio.name == "meeting.wav":
    output = folder / "transcript.txt"
else:
    output = audio.with_suffix(".txt")

output.write_text("\n".join(parts), encoding="utf-8")
print(f"\nSaved {len(' '.join(parts))} characters to {output}", flush=True)
