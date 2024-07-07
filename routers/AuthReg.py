from fastapi import APIRouter

from models.models import LoginClass, Worker
from controllers.AuthReg import loginFunc, create_worker

router = APIRouter()


@router.post('/login', tags=["Auth"])
def auth(loginData: LoginClass):
    user_id = loginFunc(loginData.login, loginData.password)
    return user_id


@router.post('/createWorker', tags=["Auth"])
def auth(worker: Worker):
    user_id = create_worker(worker)
    return user_id
