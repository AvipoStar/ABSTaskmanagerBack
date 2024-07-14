from fastapi import APIRouter

from controllers.team import create_team, get_teams, attach_worker_to_team, delete_team, create_role
from models.models import Team, AttachToTeam, Role

router = APIRouter()


@router.post("/create_team", tags=["Teams"], description="Создание новой команды")
def create_team_route(team_data: Team):
    return create_team(team_data.name)


@router.get("/get_teams/{user_id}", tags=["Teams"], description="Получение команд пользователя")
def get_team_route(user_id: int):
    return get_teams(user_id)


@router.post("/attach_worker_to_team", tags=["Teams"], description="Получение команд пользователя")
def attach_worker_to_team_route(data: AttachToTeam):
    return attach_worker_to_team(data.team_id, data.user_id)


@router.delete("/delete_team/{team_id}", tags=["Teams"])
def delete_team_route(team_id: int):
    return delete_team(team_id)


@router.post("/create_role", tags=["Teams"])
def createRole(role_data: Role):
    return create_role(role_data)
