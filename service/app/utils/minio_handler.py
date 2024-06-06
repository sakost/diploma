import asyncio

import aioboto3
from pydantic_settings import BaseSettings


class CustomBaseSettings(BaseSettings):
    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class MinioSettings(CustomBaseSettings):
    MINIO_HOST: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str

    async def upload_file(self):
        try:
            session = aioboto3.Session(
                region_name="ams3",
                aws_access_key_id="DO00DELD3LM22XYZP3MG",
                aws_secret_access_key="hQ9S0wFq/1NEWj0Ejem5aGDKWXXbLsbSO0p2YxTS6Qo",
            )

            async with session.client(
                "s3",
                endpoint_url="https://dev-s3-hedge-fund.ams3.digitaloceanspaces.com",
            ) as s3:
                #  renaming
                await s3.copy_object(
                    Bucket="dev-s3-hedge-fund",
                    CopySource="dev-s3-hedge-fund/dev-s3-hedge-fund/smth.txt",
                    Key="NewName.txt",
                )
                await s3.delete_object(Bucket="dev-s3-hedge-fund", Key="smth.txt")

                #  deleting
                await s3.delete_object(Bucket="dev-s3-hedge-fund", Key="smth.txt")

                #  uploading
                await s3.upload_file(
                    "./java.txt",
                    "dev-s3-hedge-fund",
                    "smth.txt",
                    ExtraArgs={"ACL": "public-read"},
                )

                return "smth"

        except Exception as err:
            print(f"Error initializing client: {err}")
            return "ERORO"

    async def get_all_files(self):
        session = aioboto3.Session(
            region_name="ams3",
            aws_access_key_id="DO00DELD3LM22XYZP3MG",
            aws_secret_access_key="hQ9S0wFq/1NEWj0Ejem5aGDKWXXbLsbSO0p2YxTS6Qo",
        )

        async with session.client(
            "s3",
            endpoint_url="https://dev-s3-hedge-fund.ams3.digitaloceanspaces.com",
        ) as s3:

            objects = await s3.list_objects(
                Bucket="dev-s3-hedge-fund.ams3.digitaloceanspaces.com",
            )

            # f = [obj.key async for obj in objects]
            print(objects)
            return objects


async def main():
    minio_settings = MinioSettings()
    minio_client = await minio_settings.get_all_files()
    print(minio_client)


# Run the event loop
asyncio.run(main())


# client = session.client(
#     "s3",
#     region_name="ams3",
#     endpoint_url="https://dev-s3-hedge-fund.ams3.digitaloceanspaces.com",
#     aws_access_key_id="DO00DELD3LM22XYZP3MG",
#     aws_secret_access_key="hQ9S0wFq/1NEWj0Ejem5aGDKWXXbLsbSO0p2YxTS6Qo",
# )
# async with client:
#     obj = await client.get_object(
#         Bucket="dev-s3-hedge-fund",
#         Key="https://dev-s3-hedge-fund.ams3.digitaloceanspaces.com/Screenshot%202024-05-12%20at%2019.20.46.png",
#     )
#     print(obj)
# bucket = await client.Bucket("dev-s3-hedge-fund")
# print(bucket)
# async for s3_object in bucket.objects.all():
#     print(s3_object)
