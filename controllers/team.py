from fastapi import FastAPI, Depends, HTTPException, status
import mysql.connector

from models.models import Role, AttachWorkerToTeamToRoles, ProjectDirection, Project

app = FastAPI()


def create_team(team_name: str):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )

    cursor = db.cursor()

    # Вставка новой команды
    cursor.execute("INSERT INTO team (name) VALUES (%s)", (team_name,))
    db.commit()
    team_id = cursor.lastrowid
    db.close()

    return {"team_id": team_id}


def attach_worker_to_team(data: AttachWorkerToTeamToRoles):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )

    cursor = db.cursor()

    try:
        # Проверяем, существует ли такая команда
        cursor.execute("SELECT id FROM team WHERE id = %s", (data.team_id,))
        team_exists = cursor.fetchone()
        if not team_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена")

        # Проверяем, существует ли такой работник
        cursor.execute("SELECT id FROM worker WHERE id = %s", (data.worker_id,))
        worker_exists = cursor.fetchone()
        if not worker_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Работник не найден")

        # Проверяем, не привязан ли уже работник к этой команде
        cursor.execute("SELECT id FROM worker2team WHERE team_id = %s AND worker_id = %s",
                       (data.team_id, data.worker_id))
        already_attached = cursor.fetchone()
        if already_attached:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Работник уже привязан к этой команде")

        # Добавляем запись о привязке работника к команде
        cursor.execute("INSERT INTO worker2team (team_id, worker_id) VALUES (%s, %s)", (data.team_id, data.worker_id))
        db.commit()

        return {"Seccess": True}

    except mysql.connector.Error as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка базы данных: {str(e)}")

    finally:
        cursor.close()


def delete_team(team_id: int):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )

    cursor = db.cursor()

    try:
        # Проверяем, существует ли такая команда
        cursor.execute("SELECT id FROM team WHERE id = %s", (team_id,))
        team_exists = cursor.fetchone()
        if not team_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена")

        # Удаляем привязки работников к команде
        cursor.execute("DELETE worker2team WHERE team_id = %s", (team_id,))

        # Удаляем команду
        cursor.execute("DELETE FROM team WHERE id = %s", (team_id,))
        db.commit()

        return {"detail": "Команда успешно удалена"}

    except mysql.connector.Error as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка базы данных: {str(e)}")

    finally:
        cursor.close()
        db.close()


def create_role(role: Role):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )

    cursor = db.cursor()

    # Вставка новой команды
    cursor.execute("INSERT INTO role (name) VALUES (%s)", (role.name,))
    db.commit()
    role_id = cursor.lastrowid
    cursor.execute("INSERT INTO role2team (role_id, team_id) VALUES (%s, %s)", (role_id, role.team_id))
    db.commit()
    db.close()

    return {"role_id": role_id}


def create_project_direction(projectDirection: ProjectDirection):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor(dictionary=True)

    cursor.execute("INSERT INTO project_direction (name, team_id) VALUES (%s, %s)",
                   (projectDirection.name, projectDirection.team_id))
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
    cursor.execute("INSERT INTO project (name, direction_id, team_id, isActive) VALUES (%s, %s, %s)",
                   (project.name, project.direction_id, project.team_id, True))
    db.commit()
    team_id = cursor.lastrowid
    db.close()

    if team_id:
        return {"team_id": team_id}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Не удалось создать проект")


def get_roles(team_id: int):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT r.id, r.name FROM abs.role r "
                   "JOIN abs.role2team rt on r.id = rt.role_id "
                   "WHERE rt.team_id = %s;", (team_id,))
    roles = cursor.fetchall()
    db.close()

    return {"roles": roles}
