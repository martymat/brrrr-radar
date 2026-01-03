import boto3
from botocore.exceptions import NoCredentialsError

s3 = boto3.client('s3')

def uploadFileToS3(file_path, bucket_name, key):
    try:
        s3.upload_file(file_path, bucket_name, key)
        url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
        print(f"File uploaded successfully: {url}")
        return url
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")
