
import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Load AWS configuration
load_dotenv()

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
REGION = os.getenv("AWS_DEFAULT_REGION")

LOCAL_FILE = "sample.txt"
CLOUD_FILE = "uploads/sample.txt"

# Connect to S3
s3 = boto3.client("s3", region_name=REGION)

try:
    print("Uploading file to AWS S3...")

    # Upload local file to cloud storage
    s3.upload_file(
        LOCAL_FILE,
        BUCKET_NAME,
        CLOUD_FILE
    )

    print("\nUPLOAD SUCCESSFUL!")
    print("Local file:", LOCAL_FILE)
    print("Cloud bucket:", BUCKET_NAME)
    print("Cloud location:", CLOUD_FILE)

except ClientError as error:
    print("AWS ERROR:", error.response["Error"]["Message"])

except FileNotFoundError:
    print("ERROR: Local file not found.")

except Exception as error:
    print("ERROR:", str(error))
