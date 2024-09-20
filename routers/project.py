from typing import List

from fastapi import APIRouter

from controllers.project import get_projects_in_team, get_project_info

router = APIRouter()


@router.get('/get_projects_in_team/{team_id}', tags=["Project"])
def getProjectsInTeam(team_id: int):
    result = get_projects_in_team(team_id)
    return result

@router.get('/get_project_info/{project_id}', tags=["Project"])
def getProjectInfo(project_id: int):
    result = get_project_info(project_id)
    return result
