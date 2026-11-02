
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

import sounddevice as sd
from scipy.io.wavfile import write

# Project settings
PROJECT_DIR = Path(__file__).resolve().parent
PYTHON = sys.executable
SAMPLE_RATE = 16000
CHANNELS = 1
SEGMENT_SECONDS = 10

# Store each recording separately
RECORDINGS_DIR = PROJECT_DIR / "recordings"
RECORDINGS_DIR.mkdir(exist_ok=True)

TRANSCRIBE_SCRIPT = PROJECT_DIR / "local_transcribe.py"
SUMMARY_SCRIPT = PROJECT_DIR / "meeting_summary.py"


def process_segment(audio_path):
    """Transcribe and summarize one recording segment."""
    transcript_path = audio_path.with_suffix(".txt")

    print("Transcribing audio...", flush=True)

    result = subprocess.run(
        [PYTHON, str(TRANSCRIBE_SCRIPT), str(audio_path)],
        cwd=PROJECT_DIR
    )

    if result.returncode != 0:
        print("Transcription failed. Continuing to next segment.")
        return

    if not transcript_path.exists():
        print(f"Transcript not found: {transcript_path}")
        return

    if not transcript_path.read_text(encoding="utf-8").strip():
        print("Transcript is empty; skipping summary for this segment.")
        return

    print("Generating meeting notes...", flush=True)

    result = subprocess.run(
        [PYTHON, str(SUMMARY_SCRIPT), str(transcript_path)],
        cwd=PROJECT_DIR
    )

    if result.returncode != 0:
        print("Summary generation failed.")
        return

    print("Segment completed successfully.", flush=True)


def main():
    print("Background Meeting Recorder started.")
    print("Recording in 10-second segments.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_path = RECORDINGS_DIR / f"meeting_{timestamp}.wav"

            print(f"Recording: {audio_path.name}")

            audio = sd.rec(
                int(SEGMENT_SECONDS * SAMPLE_RATE),
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                dtype="int16"
            )
            sd.wait()

            write(str(audio_path), SAMPLE_RATE, audio)
            print(f"Saved: {audio_path.name}")

            process_segment(audio_path)
            print("\nStarting next segment...\n")

    except KeyboardInterrupt:
        print("\nRecorder stopped safely.")
        print("Finalizing meeting transcript and notes...")

        result = subprocess.run(
            [PYTHON, str(PROJECT_DIR / "finish_meeting.py")],
            cwd=PROJECT_DIR
        )

        if result.returncode == 0:
            print("\nMeeting finalized successfully!")
            print("Transcript: combined_transcript.txt")
            print("Notes: combined_transcript_notes.txt")
        else:
            print("\nMeeting recording stopped, but finalization failed.")


if __name__ == "__main__":
    main()
