from minio import Minio
from fastapi import UploadFile
import io


class MinioClient:
    def __init__(self):
        self.client = Minio(
            'localhost:9000',
            access_key='minioadmin',
            secret_key='minioadmin',
            secure=False
        )
        self.bucket_name = 'memes'
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    def upload_file(self, file: UploadFile):
        try:
            self.client.put_object(
                self.bucket_name,
                file.filename,
                file.file,
                length=-1,
                part_size=10 * 1024 * 1024
            )
            return True
        except Exception as e:
            print(f"Error uploading file:\n{e}")
            return False

    def download_file(self, filename: str):
        try:
            response = self.client.get_object(self.bucket_name, filename)
            return io.BytesIO(response.read())
        except Exception as e:
            print(f"Error downloading file:\n{e}")
            return None
