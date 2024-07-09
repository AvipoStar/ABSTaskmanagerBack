from fastapi import APIRouter

from controllers.team import create_team, get_teams, attach_worker_to_team, delete_team
from controllers.worker import create_worker, get_workers_in_team
from models.models import Team, AttachToTeam, Worker

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
