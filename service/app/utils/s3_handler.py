# import asyncio
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import aioboto3
import aiobotocore
import aiobotocore.client
from dotenv import load_dotenv


load_dotenv()


class S3Settings:
    def __init__(self):
        self.S3_REGION_NAME = os.getenv("S3_REGION_NAME")
        self.S3_AWS_ACCESS_KEY_ID = os.getenv("S3_AWS_ACCESS_KEY_ID")
        self.S3_AWS_SECRET_KEY = os.getenv("S3_AWS_SECRET_KEY")
        self.S3_SERVICE_NAME = os.getenv("S3_SERVICE_NAME")
        self.S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
        self.S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


class S3Handler(S3Settings):
    def __init__(self):
        super().__init__()
        self.bucket_name = self.S3_BUCKET_NAME
        self.s3_session = aioboto3.Session(
            region_name=self.S3_REGION_NAME,
            aws_access_key_id=self.S3_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.S3_AWS_SECRET_KEY,
        )
        self.client: Optional[aiobotocore.client.AioBaseClient] = None

    @asynccontextmanager
    async def get_client(
        self,
    ) -> AsyncGenerator[aiobotocore.client.AioBaseClient, None]:
        client = await self.s3_session.client(
            service_name=self.S3_SERVICE_NAME,
            endpoint_url=self.S3_ENDPOINT_URL,
        ).__aenter__()
        try:
            yield client
        except Exception as err:
            print(f"Error in S3 client operations: {err}")
        finally:
            await client.__aexit__(None, None, None)

    async def upload_file(
        self, file_path: str, key: str, extra_args: dict = {}
    ) -> None:
        async with self.get_client() as client:
            try:
                await client.upload_file(
                    file_path,
                    self.bucket_name,
                    key,
                    ExtraArgs=extra_args,
                )
            except Exception as err:
                raise Exception(f"Error uploading file: {err}")

    async def delete_file(self, key: str) -> None:
        async with self.get_client() as client:
            try:
                await client.delete_object(Bucket=self.bucket_name, Key=key)
            except Exception as err:
                raise Exception(f"Error deleting file: {err}")

    async def rename_file(self, source_file_name: str, new_file_name: str) -> None:
        async with self.get_client() as client:
            try:
                await client.copy_object(
                    Bucket=self.bucket_name,
                    CopySource=f"{self.bucket_name}/{self.bucket_name}/{source_file_name}",
                    Key=new_file_name,
                )
                await self.delete_file(source_file_name)
            except Exception as err:
                raise Exception(f"Error renaming file: {err}")


s3_handler = S3Handler()


# Example usage


# async def main():
#     s3_handler = S3Handler()
# await s3_handler.upload_file(
#     "./java.txt", s3_handler.bucket_name, "sosi.txt", {"ACL": "public-read"}
# )
# await s3_handler.rename_file("whitepapers/whitepaper.pdf", "NewName.txt")
# await settings.delete_file("dev-s3-hedge-fund", "smth.txt")


# if __name__ == "__main__":
#     asyncio.run(main())
