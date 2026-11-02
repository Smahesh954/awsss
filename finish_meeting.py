
import subprocess
import sys
from pathlib import Path

folder = Path(__file__).resolve().parent
python = sys.executable

steps = [
    ("Combining transcript segments", "combine_meeting.py"),
]

for description, script in steps:
    print(f"\n{'=' * 50}")
    print(description)
    print("=" * 50)

    result = subprocess.run(
        [python, str(folder / script)],
        cwd=folder
    )

    if result.returncode != 0:
        raise SystemExit(f"Failed: {script}")

print("\nGenerating combined meeting notes...")

result = subprocess.run(
    [
        python,
        str(folder / "meeting_summary.py"),
        str(folder / "combined_transcript.txt")
    ],
    cwd=folder
)

if result.returncode != 0:
    raise SystemExit("Meeting summary generation failed.")

print("\nMeeting processing complete!")
print("Transcript: combined_transcript.txt")
print("Notes: combined_transcript_notes.txt")
