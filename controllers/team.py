from fastapi import FastAPI, Depends, HTTPException, status
import mysql.connector

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


def get_teams(user_id: int):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor(dictionary=True)

    # Запрос на получение всех компаний, к которым привязан пользователь
    cursor.execute("""
        SELECT t.id, t.name
        FROM team t
        JOIN worker2team wt ON t.id = wt.team_id
        WHERE wt.worker_id = %s
    """, (user_id,))
    teams = cursor.fetchall()

    db.close()

    return {"teams": teams}


def attach_worker_to_team(team_id: int, worker_id: int):
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

        # Проверяем, существует ли такой работник
        cursor.execute("SELECT id FROM worker WHERE id = %s", (worker_id,))
        worker_exists = cursor.fetchone()
        if not worker_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Работник не найден")

        # Проверяем, не привязан ли уже работник к этой команде
        cursor.execute("SELECT id FROM worker2team WHERE team_id = %s AND worker_id = %s", (team_id, worker_id))
        already_attached = cursor.fetchone()
        if already_attached:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Работник уже привязан к этой команде")

        # Добавляем запись о привязке работника к команде
        cursor.execute("INSERT INTO worker2team (team_id, worker_id) VALUES (%s, %s)", (team_id, worker_id))
        db.commit()

        # Получаем обновленные данные о команде
        cursor.execute("SELECT id, name FROM team WHERE id = %s", (team_id,))
        team_data = cursor.fetchone()

        return team_data

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
