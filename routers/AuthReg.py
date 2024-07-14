from fastapi import APIRouter

from models.models import LoginClass, Worker
from controllers.AuthReg import loginFunc

router = APIRouter()


@router.post('/login', tags=["Auth"])
def auth(loginData: LoginClass):
    worker = loginFunc(loginData.login, loginData.password)
    return worker
