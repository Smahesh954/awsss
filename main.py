
import subprocess
import sys
from pathlib import Path

folder = Path(__file__).resolve().parent
python = sys.executable

steps = [
    ("Recording audio", "recorder.py"),
    ("Transcribing audio", "local_transcribe.py"),
    ("Generating AI meeting notes", "meeting_summary.py"),
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
        print(f"\nERROR: {script} failed.")
        raise SystemExit(result.returncode)

print("\nAll steps completed successfully!")
print("Audio: meeting.wav")
print("Transcript: transcript.txt")
print("Meeting notes: meeting_notes.txt")
