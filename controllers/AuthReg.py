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
    cursor.execute("SELECT password FROM worker WHERE login = %s", (login,))
    result = cursor.fetchone()
    print(f'\nresult {result}\n')
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
            return {"worker": worker}
    else:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
