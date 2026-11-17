
import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError, NoCredentialsError

# Load AWS credentials from .env
load_dotenv()

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
REGION = os.getenv("AWS_DEFAULT_REGION")

print("Connecting to AWS S3...")

try:
    # Create S3 client
    s3 = boto3.client(
        "s3",
        region_name=REGION
    )

    # Test bucket access
    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        MaxKeys=10
    )

    print("\n================================")
    print("     AWS CONNECTION SUCCESS")
    print("================================")
    print("Bucket:", BUCKET_NAME)
    print("Region:", REGION)

    print("\nFiles stored in cloud:")

    files = response.get("Contents", [])

    if files:
        for file in files:
            print("-", file["Key"])
    else:
        print("No files found. Bucket is empty.")

except NoCredentialsError:
    print("ERROR: AWS credentials not found.")

except ClientError as e:
    print("AWS ERROR:", e.response["Error"]["Message"])

except Exception as e:
    print("ERROR:", str(e))
