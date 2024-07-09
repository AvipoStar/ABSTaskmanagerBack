from fastapi import APIRouter

from models.models import LoginClass, Worker
from controllers.AuthReg import loginFunc

router = APIRouter()


@router.post('/login', tags=["Auth"])
def auth(loginData: LoginClass):
    user_id = loginFunc(loginData.login, loginData.password)
    return user_id

