from fastapi import FastAPI, File, UploadFile, HTTPException
from minio_client import MinioClient

app = FastAPI()
minio_client = MinioClient()


@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    result = minio_client.upload_file(file)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to upload file")
    return {"filename": file.filename}

@app.get("/download_file/{filename}")
async def get_file(filename: str):
    file = minio_client.download_file(filename)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file