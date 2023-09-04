import uuid

from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse
from config import config
from loguru import logger
import os
from pathlib import Path
import aiofiles
from schemas.system.file import FileIn
from models.systerm_models import FileInfo


class FileServer:
    @staticmethod
    async def upload(file: UploadFile):
        if not file:
            raise FileNotFoundError("选择上传文件")
        file_dir = config.TEST_FILES_DIR
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        extend_file = file.filename.split('.')
        extend_name = extend_file[-1] if len(extend_file) else None
        file_name = f'{str(uuid.uuid4()).replace("-", "").upper()}'
        if extend_name:
            file_name = f"{file_name}.{extend_name}"
        abs_file_path = Path(file_dir).joinpath(file_name).as_posix()
        contents = await file.read()
        file_size = len(contents) / 1024
        async with aiofiles.open(abs_file_path, "wb") as f:
            await f.write(contents)
        file_params = FileIn(id=str(uuid.uuid4()).replace("-", ""),
                             name=file_name,
                             file_path=abs_file_path,
                             extend_name=extend_name,
                             original_name=file.filename,
                             file_size=str(file_size),
                             contents_type=file.content_type)
        file_info = await FileInfo.create(file_params.model_dump())
        logger.info(f"文件保存--> {abs_file_path}")
        file_id = file_info.id
        data = {
            'id': file_id,
            'url': f'/file/download/{file_id}',
            'name': file.filename,
            'original_name': file.filename,
        }
        return data

