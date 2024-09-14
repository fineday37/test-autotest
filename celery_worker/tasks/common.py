
from celery_worker.worker import celery
from celery_worker.base import run_async
from schemas.api.projectquery import ProjectIn
from services.api.project import ProjectService


@celery.task
def add(i):
    return 1 + i


@celery.task
def save_project(params):
    data = ProjectIn(**params)
    run_async(ProjectService.save_or_update(data))
