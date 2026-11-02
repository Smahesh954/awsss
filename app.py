
import boto3
from botocore.exceptions import ClientError

REGION = "ap-south-1"

try:
    s3 = boto3.client("s3", region_name=REGION)
    response = s3.list_buckets()

    print("AWS connection successful!")
    print("Your S3 buckets:")

    for bucket in response["Buckets"]:
        print("-", bucket["Name"])

except ClientError as error:
    print("AWS error:", error)
