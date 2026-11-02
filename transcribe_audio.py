import boto3
import time
import json
import urllib.request
from botocore.exceptions import ClientError

TRANSCRIBE_REGION = "ap-south-1"
S3_REGION = "us-east-1"

BUCKET_NAME = "ai-meeting-notes-mahesh-2026"
AUDIO_KEY = "recordings/meeting.wav"
JOB_NAME = "meeting-transcription-002"

transcribe = boto3.client(
    "transcribe",
    region_name=TRANSCRIBE_REGION,
)

s3 = boto3.client("s3", region_name=S3_REGION)

try:
    print("Checking audio file in S3...")

    s3.head_object(Bucket=BUCKET_NAME, Key=AUDIO_KEY)

    print("Audio found. Starting transcription...")

    transcribe.start_transcription_job(
        TranscriptionJobName=JOB_NAME,
        Media={
            "MediaFileUri": f"s3://{BUCKET_NAME}/{AUDIO_KEY}"
        },
        MediaFormat="wav",
        LanguageCode="en-US",
    )

    while True:
        response = transcribe.get_transcription_job(
            TranscriptionJobName=JOB_NAME
        )

        job = response["TranscriptionJob"]
        status = job["TranscriptionJobStatus"]

        print("Status:", status)

        if status == "COMPLETED":
            url = job["Transcript"]["TranscriptFileUri"]

            with urllib.request.urlopen(url) as result:
                data = json.loads(result.read().decode("utf-8"))

            transcript = data["results"]["transcripts"][0]["transcript"]

            with open("transcript.txt", "w", encoding="utf-8") as file:
                file.write(transcript)

            print("\nTranscript:")
            print(transcript)
            print("\nSaved as transcript.txt")
            break

        if status == "FAILED":
            print("Transcription failed:", job.get("FailureReason"))
            break

        time.sleep(5)

except Exception as error:
    print("ERROR:", error)