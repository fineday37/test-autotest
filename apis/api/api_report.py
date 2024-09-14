from fastapi import APIRouter

from schemas.api.api_report import TestReportDetailQuery, TestReportQuery
from services.api.api_report import ReportService
from corelibs.http_response import partner_success

router = APIRouter()


@router.post("/list", description="获取报告列表")
async def getReportList(params: TestReportQuery):
    data = await ReportService.list(params)
    return partner_success(data)


@router.post("/getReportDetail", description="获取报告详情")
async def getReportDetail(params: TestReportDetailQuery):
    data = await ReportService.detail(params)
    return partner_success(data)


@router.post("/getReportStatistics", description="获取报告统计")
async def getReportStatistics(params: TestReportDetailQuery):
    data = await ReportService.statistics(params)
    return partner_success(data)
