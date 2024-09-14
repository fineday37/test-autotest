import asyncio
import datetime
import traceback
import uuid
from abc import ABC
from celery import Celery, Task
from celery.worker.request import Request

from config import config
from corelibs.local import g
from corelibs.logger import logger
from db import init_redis_pool
from schemas.job.task_record import TaskRecordIn
from services.job.task_record import TaskRecordServer
from utils.async_converter import AsyncIOPool
from celery._state import _task_stack


class TaskRequest(Request):
    """重写task request 设置 trace_id 这里可以设置所有透传过来的参数"""

    def __init__(self, *args, **kwargs):
        super(TaskRequest, self).__init__(*args, **kwargs)
        self.set_trace_id()

    def set_trace_id(self):
        """这里为了设置消息发送是的trace_id能与请求保持一致特殊处理"""
        trace_id = self.request_dict.get("trace_id", str(uuid.uuid4()))
        g.trace_id = trace_id


def create_celery():
    """
    job 初始类
    :return:
    """

    class ContextTask(Task, ABC):
        Request = TaskRequest

        def delay(self, *args, **kwargs):
            return self.apply_async(args, kwargs)

        def apply_async(self, args=None, kwargs=None, task_id=None, producer=None,
                        link=None, link_error=None, shadow=None, **options):
            __task_type = options.get("__task_type", None)
            __task_type = __task_type if __task_type else 10
            headers = {"headers": {"trace_id": g.trace_id}, "__task_type": __task_type}
            if options:
                options.update(headers)
            else:
                options = headers
            return super(ContextTask, self).apply_async(args, kwargs, task_id, producer, link, link_error,
                                                        shadow, **options)

        def on_success(self, retval, task_id, args, kwargs):
            """任务成功时回调"""
            logger.info("on_success")
            self.handel_task_record("SUCCESS", str(retval))
            return super(ContextTask, self).on_success(retval, task_id, args, kwargs)

        def on_failure(self, exc, task_id, args, kwargs, einfo):
            """任务失败时回调"""
            logger.info("on_failure")
            self.handel_task_record("FAILURE", str(exc), einfo.traceback)
            return super(ContextTask, self).on_failure(exc, task_id, args, kwargs, einfo)

        def handel_task_record(self, status: str, result: str, err: str = None):
            """
            处理任务记录
            :param status: 状态
            :param result: 结果
            :param err: 异常信息
            :return:
            """
            try:
                record_task_info = AsyncIOPool.run_in_pool(TaskRecordServer.get_task_record_by_id(self.request.id))
                if record_task_info:
                    record_task_info["status"] = status
                    record_task_info["result"] = result
                    record_task_info["traceback"] = err
                    record_task_info["end_time"] = datetime.datetime.now()
                    params = TaskRecordIn(**record_task_info)
                    AsyncIOPool.run_in_pool(TaskRecordServer.save_or_update(params))
            except:
                logger.error(f"handel task  result error task id [{self.request.id}]:\n{traceback.format_exc()}")

        def __call__(self, *args, **kwargs):
            """重写call方法 支持异步函数的运行"""
            g.trace_id = self.request.trace_id
            _task_stack.push(self)
            self.push_request(args=args, kwargs=kwargs)
            g.redis = AsyncIOPool.run_in_pool(init_redis_pool())
            try:
                if asyncio.iscoroutinefunction(self.run):
                    return AsyncIOPool.run_in_pool(self.run(*args, **kwargs))
                else:
                    return self.run(*args, **kwargs)
            finally:
                self.pop_request()
                _task_stack.pop()

    _celery_: Celery = Celery("zerorunner-job-worker", task_cls=ContextTask)
    _celery_.config_from_object(config)

    return _celery_


celery = create_celery()
