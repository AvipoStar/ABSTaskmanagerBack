from typing import List

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


def get_roles_in_team(team_id: int):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT r.id, r.name "
                   "FROM role2team rt "
                   "JOIN role r ON r.id = rt.role_id "
                   "WHERE rt.team_id = %s ", (team_id,))
    roles = cursor.fetchall()

    db.close()

    return {"roles": roles}


def get_teams(user_id: int):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor(dictionary=True)

    print(f'\nuser_id: {user_id}\n')

    cursor.execute("""
        SELECT  t.id as team_id, 
                t.name as team_name, 
                pd.id as project_direction_id, 
                pd.name as project_direction_name, 
                p.id as project_id, 
                p.name as project_name
        FROM team t
        JOIN worker2team wt ON t.id = wt.team_id
        JOIN project_direction pd ON t.id = pd.team_id
        JOIN project p ON pd.id = p.direction_id
        JOIN worker2direction wd ON pd.id = wd.direction_id
        WHERE wt.worker_id = %s AND wd.worker_id = %s
    """, (user_id, user_id))

    teams = []
    current_team = None
    current_project_direction = None

    for row in cursor.fetchall():
        print(f'row {row}')
        if not current_team or current_team['team_id'] != row['team_id']:
            current_team = {
                'team_id': row['team_id'],
                'team_name': row['team_name'],
                'projectDirections': []
            }
            teams.append(current_team)
            current_project_direction = None

        if not current_project_direction or current_project_direction['project_direction_id'] != row[
            'project_direction_id']:
            current_project_direction = {
                'project_direction_id': row['project_direction_id'],
                'project_direction_name': row['project_direction_name'],
                'projects': []
            }
            current_team['projectDirections'].append(current_project_direction)

        current_project_direction['projects'].append({
            'project_id': row['project_id'],
            'project_name': row['project_name']
        })

    db.close()
    return {"teams": teams}


def change_favorite_project(user_id: int, project_id: int):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="abs"
        )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM favorite_project WHERE worker_id = %s AND project_id = %s", (user_id, project_id))
        favorite = cursor.fetchone()
        if favorite:
            cursor.execute("DELETE FROM favorite_project WHERE worker_id = %s AND project_id = %s",
                           (user_id, project_id))
        else:
            cursor.execute("INSERT INTO favorite_project (worker_id, project_id) VALUES (%s, %s)",
                           (user_id, project_id))
        db.commit()
        db.close()
        return {"success": True}
    except mysql.connector.Error as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Не удалось поменять статус проекта")


def add_roles(user_id: int, team_id: int, role_ids: List[int]):
    if not isinstance(role_ids, list) or not all(isinstance(role, int) for role in role_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="role_ids должен быть списком целых чисел")

    db = None
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="abs"
        )
        cursor = db.cursor()
        for role in role_ids:
            cursor.execute("INSERT INTO worker2team (team_id, worker_id, role_id) VALUES (%s, %s, %s)",
                           (team_id, user_id, role))
        db.commit()
        return {"success": True}
    except mysql.connector.Error as error:
        if db:
            db.rollback()  # Откат транзакции в случае ошибки
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Не удалось добавить роль работнику: {str(error)}")
    finally:
        if db:
            db.close()  # Закрываем соединение с базой данных
