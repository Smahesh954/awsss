import boto3
from botocore.exceptions import ClientError

REGION = "ap-south-1"
BUCKET_NAME = "ai-meeting-notes-mahesh-2026"
AUDIO_FILE = "meeting.wav"

try:
    s3 = boto3.client("s3", region_name=REGION)

    s3.upload_file(
        AUDIO_FILE,
        BUCKET_NAME,
        "recordings/meeting.wav"
    )

    print("Audio uploaded successfully to AWS S3!")
    print(f"s3://{BUCKET_NAME}/recordings/meeting.wav")

except (ClientError, FileNotFoundError) as error:
    print("Upload failed:", error)
