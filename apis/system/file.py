from fastapi import APIRouter, UploadFile, File
from services.system.file import FileServer
from corelibs.http_response import partner_success
from schemas.system.file import FileId

router = APIRouter()


@router.post('/upload', description="上传文件")
async def upload(file: UploadFile = File(...)):
    result = await FileServer.upload(file)
    return partner_success(result)


@router.post('/download/{file_id}', description="文件下载")
async def download(file_id: str):
    result = await FileServer.download(file_id)
    return result


@router.post('/getFileById', description="根据id获取文件地址")
async def get_file_by_id(params: FileId):
    return await FileServer.get_file_by_id(params)


@router.post('/deleted', description="文件删除")
async def deleted(params: FileId):
    data = await FileServer.deletes(params)
    return {"code": data, "success": "删除成功"}
