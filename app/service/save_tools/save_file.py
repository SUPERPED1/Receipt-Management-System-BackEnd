import aiofiles
from fastapi import UploadFile
from pathlib import Path
import uuid

async def save_file(file:UploadFile):
    folder_path = Path("uploads")
    folder_path.mkdir(parents=True, exist_ok=True)
    
    file_name = str(uuid.uuid4())
    path = f"uploads/{file_name}.jpg"
    async with aiofiles.open(path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    return path