
from pathlib import Path

folder = Path(__file__).resolve().parent
recordings_dir = folder / "recordings"

# Find transcripts and exclude generated notes files.
transcript_files = sorted(
    path for path in recordings_dir.glob("meeting_*.txt")
    if not path.name.endswith("_notes.txt")
)

if not transcript_files:
    raise FileNotFoundError("No segment transcripts found.")

combined_parts = []
empty_files = []

for transcript_file in transcript_files:
    text = transcript_file.read_text(encoding="utf-8").strip()

    if not text:
        empty_files.append(transcript_file.name)
        continue

    combined_parts.append(
        f"[Segment: {transcript_file.stem}]\n{text}"
    )

if not combined_parts:
    raise ValueError("All transcript files are empty.")

output_file = folder / "combined_transcript.txt"
output_file.write_text(
    "\n\n".join(combined_parts) + "\n",
    encoding="utf-8"
)

print(f"Combined {len(combined_parts)} transcript segments.")
print(f"Saved to: {output_file}")

if empty_files:
    print("\nWarning: These empty transcripts were skipped:")
    for name in empty_files:
        print(f" - {name}")
