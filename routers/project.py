from typing import List

from fastapi import APIRouter

from controllers.project import create_project, change_favorite_project, get_projects_in_team, create_project_direction, \
    get_project_directions_in_team
from models.models import Project, ProjectDirection

router = APIRouter()


@router.get('/get_project_directions_in_team/{team_id}', tags=["Project"])
def getProjectDirectionInTeam(team_id: int):
    project_directions = get_project_directions_in_team(team_id)
    return project_directions


@router.post('/create_project_direction', tags=["Project"], response_model=int)
def createProjectDirection(name_direction: str):
    direction_id = create_project_direction(name_direction)
    return direction_id


@router.post('/create_project', tags=["Project"], response_model=int)
def createProject(project: Project):
    user_id = create_project(project)
    return user_id


@router.post('/change_favorite_project', tags=["Project"], response_model=bool)
def changeFavoriteProject(user_id: int, project_id: int):
    result = change_favorite_project(user_id, project_id)
    return result


@router.post('/get_projects_in_team', tags=["Project"])
def getProjectsInTeam(team_id: int):
    result = get_projects_in_team(team_id)
    print(f'projects {result}')
    return result
