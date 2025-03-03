import argparse
from helper import upload_folder

def main():
    """
    Parses command-line arguments and starts the S3 upload process.
    """
    parser = argparse.ArgumentParser(description="Upload a folder to S3 while preserving folder structure.")
    parser.add_argument("--src", required=True, help="Local folder path to upload.")
    parser.add_argument("--dest", required=True, help="S3 bucket name or ARN.")

    args = parser.parse_args()

    upload_folder(args.src, args.dest)

if __name__ == "__main__":
    main()
