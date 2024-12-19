import boto3
from botocore.exceptions import ClientError
from typing import Generator
from repository.base_storage import BaseStorage

class S3Storage(BaseStorage):
    def __init__(self, bucket_name: str, aws_access_key_id: str, aws_secret_access_key: str, region_name: str):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def save(self, filename: str, data: bytes) -> bool:
        """Save file to S3"""
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=data
            )
            return True
        except ClientError as e:
            print(f"Error saving to S3: {str(e)}")
            return False

    def load_once(self, filename: str) -> bytes:
        """Load entire file from S3"""
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=filename
            )
            return response['Body'].read()
        except ClientError as e:
            print(f"Error loading from S3: {str(e)}")
            return b''

    def load_stream(self, filename: str) -> Generator:
        """Stream file from S3"""
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=filename
            )
            for chunk in response['Body'].iter_chunks(chunk_size=8192):
                yield chunk
        except ClientError as e:
            print(f"Error streaming from S3: {str(e)}")
            yield b''

    def download(self, filename: str, target_filepath: str) -> bool:
        """Download file from S3 to local path"""
        try:
            self.s3_client.download_file(
                self.bucket_name,
                filename,
                target_filepath
            )
            return True
        except ClientError as e:
            print(f"Error downloading from S3: {str(e)}")
            return False

    def exists(self, filename: str) -> bool:
        """Check if file exists in S3"""
        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=filename
            )
            return True
        except ClientError:
            return False

    def delete(self, filename: str) -> bool:
        """Delete file from S3"""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=filename
            )
            return True
        except ClientError as e:
            print(f"Error deleting from S3: {str(e)}")
            return False