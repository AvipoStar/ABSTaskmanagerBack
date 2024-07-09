import mysql.connector
from fastapi import FastAPI, HTTPException, status

from models.models import Project

app = FastAPI()


def get_project_directions():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor(dictionary=True)

    # Запрос на получение всех направлений проектов в команде
    cursor.execute("SELECT *  FROM project_directions")
    project_directions = cursor.fetchall()

    db.close()

    return {"project_directions": project_directions}


def create_project_direction(name_direction: str):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor(dictionary=True)

    # Запрос на получение всех направлений проектов в команде
    cursor.execute("INSERT INTO project_directions (name) VALUES (%s)", (name_direction))
    db.commit()
    project_direction_id = cursor.lastrowid

    db.close()

    return {"project_direction_id": project_direction_id}


def create_project(project: Project):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )

    cursor = db.cursor()
    cursor.execute("INSERT INTO project (name, direction_id, team_id) VALUES (%s, %s)",
                   (project.name, project.direction_id, project.team_id))
    db.commit()
    team_id = cursor.lastrowid
    db.close()

    if team_id:
        return {"team_id": team_id}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Не удалось создать проект")


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


def get_projects_in_team(team_id: int):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor(dictionary=True)

    # Запрос на получение всех проектов в команде
    cursor.execute("""
        SELECT p.id, p.name, p.direction_id, p.team_id 
        FROM project p 
        JOIN team t ON t.id = p.team_id 
        WHERE wt.worker_id = %s
    """, (team_id,))
    projects = cursor.fetchall()

    db.close()

    return {"projects": projects}
