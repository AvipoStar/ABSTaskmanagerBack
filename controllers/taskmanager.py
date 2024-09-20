import mysql

from models.models import Column, Task


def create_or_update_column(column: Column):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )

    cursor = db.cursor()

    if column.id:
        cursor.execute("UPDATE `column` SET name = %s, project_id = %s WHERE id = %s",
                       (column.name, column.project_id, column.id))
        db.commit()
        column_id = column.id
    else:
        cursor.execute("SELECT MAX(c.serial_number) AS max_serial_number FROM `column` c WHERE c.project_id = %s;",
                       (column.project_id,))
        last_column_serial_number = cursor.fetchone()
        cursor.execute("INSERT INTO `column` (name, project_id, serial_number) VALUES (%s, %s, %s)",
                       (column.name, column.project_id,
                        (last_column_serial_number[0] + 1) if last_column_serial_number[0] else 1))
        db.commit()
        column_id = cursor.lastrowid

    db.close()

    return {"column_id": column_id}


def create_or_update_task(task: Task):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )

    cursor = db.cursor()

    if task.id:
        cursor.execute("UPDATE `task` SET name = %s, column_id = %s WHERE id = %s",
                       (task.name, task.column_id, task.id))
        db.commit()
        task_id = task.id
    else:
        cursor.execute("SELECT MAX(t.serial_number) AS max_serial_number FROM `task` t WHERE t.column_id = %s;",
                       (task.column_id,))
        last_task_serial_number = cursor.fetchone()
        cursor.execute("INSERT INTO `task` (name, column_id, serial_number) VALUES (%s, %s, %s)",
                       (task.name, task.column_id,
                        (last_task_serial_number[0] + 1) if last_task_serial_number[0] else 1))
        db.commit()
        task_id = cursor.lastrowid

    db.close()

    return {"task_id": task_id}
