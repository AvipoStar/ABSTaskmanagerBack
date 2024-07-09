from fastapi import APIRouter

from controllers.project import create_project, change_favorite_project, get_projects_in_team, create_project_direction, \
    get_project_directions
from models.models import Project

router = APIRouter()


@router.get('/get_project_direction', tags=["Project"])
def getProjectDirection():
    project_directions = get_project_directions()
    return project_directions


@router.post('/create_project_direction', tags=["Project"])
def createProjectDirection(name_direction: str):
    direction_id = create_project_direction(name_direction)
    return direction_id


@router.post('/create_project', tags=["Project"])
def createProject(project: Project):
    user_id = create_project(project)
    return user_id


@router.post('/change_favorite_project', tags=["Project"])
def changeFavoriteProject(project: Project):
    result = change_favorite_project(project)
    return result


@router.post('/get_projects_in_team', tags=["Project"])
def getProjectsInTeam(project: Project):
    result = get_projects_in_team(project)
    return result
