from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime


class LoginClass(BaseModel):
    login: str
    password: str


class Task(BaseModel):
    id: Optional[int]
    creation_date_time: Optional[datetime]
    priority_id: Optional[int]
    deadline: Optional[datetime]
    description: Optional[str]
    serial_number: Optional[int]
    is_done: Optional[bool]
    name: str
    column_id: int
    creator_id: int


class Attachment2Task(BaseModel):
    id: int
    path: str
    task_id: int


class Priority(BaseModel):
    id: int
    name: str
    color: str


class Column(BaseModel):
    id: Optional[int]
    serial_number: Optional[int]
    name: str
    project_id: int


class Project(BaseModel):
    id: Optional[int]
    name: str
    direction_id: int
    team_id: int
    isActive: bool


class ProjectDirection(BaseModel):
    id: Optional[int]
    name: str
    team_id: int


class Worker(BaseModel):
    id: Optional[int]
    login: str
    password: str
    fio: str
    mail: Optional[str]


class Worker2Direction(BaseModel):
    id: int
    worker_id: int
    direction_id: int


class Worker2Team(BaseModel):
    id: int
    team_id: int
    worker_id: int


class Team(BaseModel):
    id: Optional[int]
    name: str


class AttachToTeam(BaseModel):
    user_id: int
    team_id: int


class Role(BaseModel):
    id: Optional[int]
    name: str
    team_id: int


class AttachWorkerToTeamToRoles(BaseModel):
    worker_id: int
    team_id: int
    role_ids: list[int]


class Token(BaseModel):
    token: str


class AddRoles(BaseModel):
    user_id: int
    team_id: int
    role_ids: List[int]
