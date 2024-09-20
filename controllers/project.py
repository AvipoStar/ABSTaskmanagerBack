import mysql.connector
from fastapi import FastAPI

app = FastAPI()


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
        SELECT p.id, p.name, p.direction_id, p.team_id, p.isActive 
        FROM project p 
        JOIN team t ON t.id = p.team_id 
        WHERE t.id = %s
    """, (team_id,))
    projects = cursor.fetchall()
    db.close()

    print(f'\n projects: {projects}\n')

    return {"projects": projects}


def get_project_info(project_id: int):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor(dictionary=True)

    # Получение информации о проекте
    cursor.execute("""
        SELECT id, name, direction_id, team_id, isActive
        FROM project
        WHERE id = %s;
    """, (project_id,))
    project = cursor.fetchone()

    if not project:
        db.close()
        return {"error": "Project not found"}

    # Получение информации о колонках проекта
    cursor.execute("""
        SELECT id, name, project_id, serial_number
        FROM `column`
        WHERE project_id = %s
        ORDER BY serial_number;
    """, (project_id,))
    columns = cursor.fetchall()

    # Получение информации о задачах
    column_ids = [col['id'] for col in columns]
    if column_ids:
        cursor.execute("""
            SELECT id, name, description, column_id, serial_number, creationd_date_time, deadline, priority_id, is_done, creator_id, parent_task_id
            FROM task
            WHERE column_id IN (%s)
            ORDER BY column_id, serial_number;
        """ % ','.join(str(id) for id in column_ids))
        tasks = cursor.fetchall()
    else:
        tasks = []

    # Организация задач по колонкам
    for column in columns:
        column['tasks'] = [task for task in tasks if task['column_id'] == column['id']]

    db.close()

    return {
        "project_info": project,
        "columns": columns
    }
