import mysql.connector
from fastapi import FastAPI, HTTPException, status

from models.models import Worker

app = FastAPI()


# Аутентификация пользователя
def loginFunc(login: str, password: str):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )

    cursor = db.cursor()
    cursor.execute("SELECT id, password FROM worker WHERE login = %s", (login,))
    result = cursor.fetchone()
    if result:
        user_id, stored_password = result
        if password != stored_password:
            db.close()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль")
        else:
            db.close()
            return {"worker_id": user_id}
    else:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
