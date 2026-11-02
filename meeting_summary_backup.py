
from pathlib import Path
from datetime import datetime
import requests

folder = Path(__file__).resolve().parent
transcript_file = folder / "transcript.txt"
output_file = folder / "meeting_notes.txt"

MODEL = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"

if not transcript_file.exists():
    raise FileNotFoundError("transcript.txt was not found.")

transcript = transcript_file.read_text(encoding="utf-8").strip()

if not transcript:
    raise ValueError("transcript.txt is empty.")

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

print("Sending transcript to local AI model...")

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
