import asyncio
from typing import Union

import boto3
from botocore.exceptions import (
    BotoCoreError,
    ConnectionError,
    HTTPClientError,
    NoCredentialsError,
)

from exceptions import S3ConnectionError, S3FileUploadError
from storages import S3StorageInterface


class S3StorageClient(S3StorageInterface):
    def __init__(
        self, endpoint_url: str, access_key: str, secret_key: str, bucket_name: str
    ):
        self._endpoint_url = endpoint_url
        self._access_key = access_key
        self._secret_key = secret_key
        self._bucket_name = bucket_name

        self._client = boto3.client(
            "s3",
            endpoint_url=self._endpoint_url,
            aws_access_key_id=self._access_key,
            aws_secret_access_key=self._secret_key,
        )

    async def upload_file(
        self, file_name: str, file_data: Union[bytes, bytearray]
    ) -> None:
        loop = asyncio.get_running_loop()
        try:
            await loop.run_in_executor(
                None,
                lambda: self._client.put_object(
                    Bucket=self._bucket_name,
                    Key=file_name,
                    Body=file_data,
                    ContentType="image/jpeg",
                ),
            )
        except (ConnectionError, HTTPClientError, NoCredentialsError) as e:
            raise S3ConnectionError(f"Failed to connect to S3 storage: {str(e)}") from e
        except BotoCoreError as e:
            raise S3FileUploadError(f"Failed to upload to S3 storage: {str(e)}") from e

    def get_file_url(self, file_name: str) -> str:
        """
        Generate a public URL for a file stored in the S3-compatible storage.

        Args:
            file_name (str): The name of the file stored in the bucket.

        Returns:
            str: The full URL to access the file.
        """
        return f"{self._endpoint_url}/{self._bucket_name}/{file_name}"
