
from pathlib import Path
from faster_whisper import WhisperModel

folder = Path(__file__).resolve().parent
audio = folder / "meeting.wav"

print("Loading base model...", flush=True)
model = WhisperModel("base", device="cpu", compute_type="int8")

print("Transcribing...", flush=True)
segments, info = model.transcribe(
    str(audio),
    beam_size=5,
    vad_filter=False,
    condition_on_previous_text=False,
    language="en",
)

parts = []
for segment in segments:
    print(f"[{segment.start:.1f}s - {segment.end:.1f}s] {segment.text}", flush=True)
    parts.append(segment.text.strip())

output = folder / "transcript.txt"
output.write_text("\n".join(parts), encoding="utf-8")

print(f"\nSaved {len(' '.join(parts))} characters to {output}", flush=True)
