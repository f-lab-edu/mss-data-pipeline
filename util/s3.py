from dotenv import load_dotenv
import os
import boto3

load_dotenv()


def get_s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name=os.getenv("aws_region"),
            aws_access_key_id=os.getenv("aws_access_key"),
            aws_secret_access_key=os.getenv("aws_secret_key"),
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3


def upload_html_to_s3(s3, html, s3_path):
    try:
        s3.put_object(
            Bucket=os.getenv("s3_bucket_name"),
            Key=s3_path,
            Body=html,
            ContentType="text/html",
        )
    except Exception as e:
        print(e)
