from http.client import HTTPException
from typing import List

from fastapi import APIRouter
from pydantic import ValidationError
from starlette import status

from controllers.team import delete_team
from controllers.worker import create_worker, get_workers_in_team, get_roles_in_team, get_teams, \
    change_favorite_project, add_roles
from models.models import Worker, AddRoles

router = APIRouter()


@router.post("/create_worker", tags=["Workers"], description="Создание нового пользователя")
def create_worker_route(worker_dat: Worker):
    return create_worker(worker_dat)


@router.get("/get_workers_in_team/{team_id}", tags=["Workers"], description="Получение пользователей в команде")
def get_team_route(team_id: int):
    return get_workers_in_team(team_id)


@router.delete("/delete_team/{team_id}", tags=["Workers"])
def delete_team_route(team_id: int):
    return delete_team(team_id)


@router.get("/get_roles_in_team/{team_id}", tags=["Workers"], description="Получение ролей пользователя в команде")
def get_roles_in_team_route(team_id: int):
    return get_roles_in_team(team_id)


@router.get("/get_teams/{user_id}", tags=["Workers"], description="Получение команд пользователя")
def get_team_route(user_id: int):
    return get_teams(user_id)


@router.post('/change_favorite_project', tags=["Workers"], response_model=bool)
def changeFavoriteProject(user_id: int, project_id: int):
    result = change_favorite_project(user_id, project_id)
    return result


@router.post('/add_roles', tags=["Workers"], response_model=bool)
def addRoles(data: AddRoles):
    try:
        print(f'data {data}')  # Проверка входящих данных
        result = add_roles(data.user_id, data.team_id, data.role_ids)
        return result
    except ValidationError as e:
        print(f'Validation error: {e}')  # Печать ошибки в консоль
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
