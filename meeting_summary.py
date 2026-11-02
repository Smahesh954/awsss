
from pathlib import Path
from datetime import datetime
import sys
import requests

folder = Path(__file__).resolve().parent

# Use a supplied transcript file, or keep the original default.
transcript_file = (
    Path(sys.argv[1]) if len(sys.argv) > 1
    else folder / "transcript.txt"
)

if not transcript_file.is_absolute():
    transcript_file = folder / transcript_file

if not transcript_file.exists():
    raise FileNotFoundError(f"Transcript not found: {transcript_file}")

# Save segment notes beside the transcript; default notes stay unchanged.
if transcript_file.name == "transcript.txt":
    output_file = folder / "meeting_notes.txt"
else:
    output_file = transcript_file.with_name(
        transcript_file.stem + "_notes.txt"
    )

MODEL = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"

transcript = transcript_file.read_text(encoding="utf-8").strip()

if not transcript:
    raise ValueError(f"Transcript is empty: {transcript_file}")

prompt = f"""
You are an accurate AI meeting-notes assistant.

Analyze the transcript below. Do not invent facts, decisions,
people, tasks, owners, or deadlines.

Create these sections:
1. MEETING SUMMARY: A concise summary.
2. KEY POINTS: Important topics discussed.
3. DECISIONS: Decisions explicitly made.
4. ACTION ITEMS: Tasks, owners, and deadlines explicitly mentioned.
   If none are stated, write "No explicit action items identified."

If the transcript is casual conversation rather than a formal meeting,
describe it accurately instead of inventing meeting details.

TRANSCRIPT:
{transcript}
"""

print("Sending transcript to local AI model...", flush=True)

response = requests.post(
    OLLAMA_URL,
    json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    },
    timeout=300
)
response.raise_for_status()

ai_notes = response.json()["response"].strip()

notes = f"""AI MEETING NOTES
================
Generated: {datetime.now().strftime("%d-%m-%Y %H:%M")}
Model: {MODEL}

{ai_notes}

FULL TRANSCRIPT
===============
{transcript}
"""

output_file.write_text(notes, encoding="utf-8")

print("\nMeeting notes generated successfully!")
print("Saved to:", output_file)
print("\n" + notes)
