from fastapi import FastAPI, Depends, HTTPException, status
import mysql.connector

from models.models import Worker

app = FastAPI()


def create_worker(worker: Worker):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )

    cursor = db.cursor()

    # Проверка на уникальность имени команды
    cursor.execute("SELECT id FROM worker WHERE login = %s", (worker.login,))
    result = cursor.fetchone()
    if result:
        db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пользователь с таким логином уже существует")

    # Вставка новой команды
    cursor.execute("INSERT INTO worker (login, password, fio, mail) VALUES (%s, %s, %s, %s)",
                   (worker.login, worker.password, worker.fio, worker.mail))
    db.commit()
    worker_id = cursor.lastrowid
    db.close()

    return {"worker_id": worker_id}


def get_workers_in_team(team_id: int):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor(dictionary=True)

    # Запрос на получение всех компаний, к которым привязан пользователь
    cursor.execute("""
        SELECT w.id, w.fio, w.mail
        FROM worker w
        JOIN worker2team wt ON w.id = wt.team_id
        WHERE wt.worker_id = %s
    """, (team_id,))
    workers = cursor.fetchall()

    db.close()

    return {"workers": workers}


def delete_worker(worker_id: int):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )

    cursor = db.cursor()

    try:
        # Проверяем, существует ли такой пользователь
        cursor.execute("SELECT id FROM team WHERE id = %s", (worker_id,))
        team_exists = cursor.fetchone()
        if not team_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

        # Удаляем привязки работников к команде
        cursor.execute("DELETE FROM worker2team WHERE worker_id = %s", (worker_id,))

        # Удаляем команду
        cursor.execute("DELETE FROM worker WHERE id = %s", (worker_id,))
        db.commit()

        return {"detail": "Пользователь успешно удален"}

    except mysql.connector.Error as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка базы данных: {str(e)}")

    finally:
        cursor.close()
        db.close()


def get_roles_in_team(worker_id: int, team_id: int):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor(dictionary=True)

    # Запрос на получение всех компаний, к которым привязан пользователь
    cursor.execute("""
            SELECT w.id, w.fio, w.mail
            FROM worker2team wt
            WHERE wt.worker_id = %s AND wt.user_id = %s
        """, (team_id, worker_id))
    workers = cursor.fetchall()

    db.close()

    return {"workers": workers}
