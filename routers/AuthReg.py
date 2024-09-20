from fastapi import APIRouter

from models.models import LoginClass, Worker, Token
from controllers.AuthReg import loginFunc, getCurrentWorker

router = APIRouter()


@router.post('/login', tags=["Auth"])
def auth(loginData: LoginClass):
    worker = loginFunc(loginData.login, loginData.password)
    return worker


@router.post('/loginToken', tags=["Auth"])
def auth(token: Token):
    worker = getCurrentWorker(token.token)
    return worker
