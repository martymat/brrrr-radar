import boto3
from botocore.exceptions import NoCredentialsError

BUCKET_NAME = "brrrr-ai-photos"  # change this to your bucket name

s3 = boto3.client("s3")

def upload_file_to_s3(file_path, key):
    print(f"📤 Uploading {file_path} to s3://{BUCKET_NAME}/{key}")
    try:
        s3.upload_file(file_path, BUCKET_NAME, key)
        print(f"✅ Uploaded {file_path} to S3 as {key}")
    except FileNotFoundError:
        print("❌ File not found.")
    except NoCredentialsError:
        print("❌ AWS credentials not available.")

upload_file_to_s3("test-photo.jpg", "uploads/test-photo.jpg")