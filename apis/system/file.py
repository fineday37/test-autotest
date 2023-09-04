from fastapi import APIRouter, UploadFile, File
from services.system.file import FileServer
from corelibs.http_response import partner_success

router = APIRouter()


@router.post('/upload', description="上传文件")
async def upload(file: UploadFile = File(...)):
    result = await FileServer.upload(file)
    return partner_success(result)
