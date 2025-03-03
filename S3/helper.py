import os
import re
import boto3

def extract_bucket_name(s3_bucket: str) -> str:
    """Extracts bucket name from an S3 ARN or trims spaces from a bucket name."""
    s3_bucket = s3_bucket.strip()  # Remove any accidental whitespace

    # Extract bucket name if ARN format is used
    arn_match = re.match(r"arn:aws:s3:::(?P<bucket_name>[a-zA-Z0-9.\-_]+)$", s3_bucket)
    if arn_match:
        return arn_match.group("bucket_name")

    return s3_bucket  # If not an ARN, return the bucket name as is

def upload_folder(local_folder: str, s3_bucket: str, s3_prefix: str = ""):
    """
    Uploads the contents of a local folder to an S3 bucket while maintaining the folder structure.

    :param local_folder: Path to the local root folder to be uploaded.
    :param s3_bucket: S3 bucket name or ARN.
    :param s3_prefix: Optional prefix for the S3 keys (e.g., "backup/").
    """
    s3 = boto3.client("s3")
    bucket_name = extract_bucket_name(s3_bucket)

    for root, _, files in os.walk(local_folder):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, local_folder)
            s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")  # Ensure S3-compatible paths

            print(f"Uploading {local_file_path} to s3://{bucket_name}/{s3_key}")
            s3.upload_file(local_file_path, bucket_name, s3_key)
