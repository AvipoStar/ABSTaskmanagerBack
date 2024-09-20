import mysql.connector
from fastapi import FastAPI, HTTPException, status
from datetime import datetime, timedelta
import jwt

from models.models import Worker

app = FastAPI()

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Аутентификация пользователя
def loginFunc(login: str, password: str):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )

    cursor = db.cursor()
    cursor.execute("SELECT password FROM worker WHERE login = %s", (login,))
    result = cursor.fetchone()
    if result:
        if password != result[0]:
            db.close()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль")
        else:
            cursor.execute("SELECT id, fio, mail FROM worker WHERE login = %s", (login,))
            worker_data = cursor.fetchone()
            db.close()
            worker = {"id": worker_data[0],
                      'fio': worker_data[1],
                      'mail': worker_data[2]}

            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = createAccessToken(
                data={"sub": login, "id": worker["id"]}, expires_delta=access_token_expires
            )
            return {"worker": worker, "access_token": access_token}
    else:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")


# Генерация токена
def createAccessToken(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Авторизация пользователя по токену
def getCurrentWorker(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")
        worker_id: int = payload.get("id")
        if login is None or worker_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен")
        else:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="abs"
            )
            cursor = db.cursor()
            cursor.execute("SELECT id, fio, mail FROM worker WHERE id = %s", (worker_id,))
            result = cursor.fetchone()
            worker = {"id": result[0],
                      'fio': result[1],
                      'mail': result[2]}
            db.close()

            return {"worker": worker, "access_token": token}
    except jwt.PyJWTError:
        db.close()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен")
