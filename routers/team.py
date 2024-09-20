from fastapi import APIRouter

from controllers.team import create_team, attach_worker_to_team, delete_team, create_role, create_project_direction, \
    create_project, get_roles
from models.models import Team, AttachToTeam, Role, ProjectDirection, Project

router = APIRouter()


@router.post("/create_team", tags=["Teams"], description="Создание новой команды")
def create_team_route(team_data: Team):
    return create_team(team_data.name)


@router.post("/attach_worker_to_team", tags=["Teams"], description="Получение команд пользователя")
def attach_worker_to_team_route(data: AttachToTeam):
    return attach_worker_to_team(data.team_id, data.user_id)


@router.delete("/delete_team/{team_id}", tags=["Teams"])
def delete_team_route(team_id: int):
    return delete_team(team_id)


@router.post("/create_role", tags=["Teams"])
def createRole(role_data: Role):
    return create_role(role_data)


@router.post('/create_project_direction', tags=["Teams"])
def createProjectDirection(project_direction: ProjectDirection):
    direction_id = create_project_direction(project_direction)
    return direction_id


@router.post('/create_project', tags=["Teams"], response_model=int)
def createProject(project: Project):
    user_id = create_project(project)
    return user_id


@router.get('/get_roles/{team_id}', tags=["Teams"])
def getRoles(team_id: int):
    roles = get_roles(team_id)
    return roles
