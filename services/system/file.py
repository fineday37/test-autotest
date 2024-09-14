import uuid

from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse
from config import config
from loguru import logger
import os
from pathlib import Path
import aiofiles
from schemas.system.file import FileIn, FileId
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

    @staticmethod
    async def download(file_id: str):
        file_info = await FileInfo.get(file_id)
        if not file_info:
            logger.error(f"{file_id} 文件不存在")
            raise HTTPException(status_code=200, detail="文件不存在")
        file_dir = Path(config.TEST_FILES_DIR).joinpath(file_info.name).as_posix()
        if not os.path.isfile(file_dir):
            raise HTTPException(status_code=200, detail='文件不存在')
        return FileResponse(path=file_dir, filename=file_info.original_name)

    @staticmethod
    async def get_file_by_id(params: FileId):
        file_info = await FileInfo.get(params.id)
        if not file_info:
            logger.error("文件不存在")
            raise HTTPException(status_code=200, detail="文件不存在")
        file_dir = Path(config.TEST_FILES_DIR).joinpath(file_info.name)
        if not file_dir:
            logger.error("文件不存在")
            raise HTTPException(status_code=200, detail="文件不存在")
        data = {
            "id": file_info.id,
            "url": f'/file//download/{file_info.id}',
            "name": file_info.original_name
        }
        return data

    @staticmethod
    async def deletes(params: FileId):
        file_info = await FileInfo.get(params.id)
        abs_file_path = file_info.file_path
        os.remove(abs_file_path)
        return await FileInfo.delete(params.id, _hard=True)



