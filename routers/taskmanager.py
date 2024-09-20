from fastapi import APIRouter

from controllers.taskmanager import create_or_update_column, create_or_update_task
from models.models import Column, Task

router = APIRouter()


@router.post('/create_column', tags=["Taskmanager"])
def createColumn(column: Column):
    result = create_or_update_column(column)
    return result


@router.post('/create_task', tags=["Taskmanager"])
def createColumn(task: Task):
    result = create_or_update_task(task)
    return result
