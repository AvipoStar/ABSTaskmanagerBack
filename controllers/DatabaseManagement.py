import mysql

from models.modelsDatabasemanagment import NewTable, NewIndex, ChangeData
from typing import List, Dict, Any
from datetime import date


def getTablesColumns():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor()
    cursor.execute("SELECT TABLE_NAME, COLUMN_NAME, COLUMN_TYPE "
                   "FROM INFORMATION_SCHEMA.COLUMNS "
                   "WHERE TABLE_SCHEMA = 'abs' "
                   "ORDER BY TABLE_NAME, ORDINAL_POSITION;")
    result = cursor.fetchall()
    db.close()
    tables = {}
    for table_name, column_name, column_type in result:
        if table_name not in tables:
            tables[table_name] = []
        tables[table_name].append({"columnName": column_name, "columnType": column_type})

    transformed_result = [{"tableName": table_name, "tableColumns": columns} for table_name, columns in tables.items()]

    return {"result": transformed_result}


def getTableColumnsInfo(tableName: str):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor()
    cursor.execute("SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, EXTRA "
                   "FROM INFORMATION_SCHEMA.COLUMNS "
                   "WHERE TABLE_NAME = %s AND TABLE_SCHEMA = 'abs';", (tableName,))
    result = cursor.fetchall()
    db.close()
    tables = []
    for COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, EXTRA in result:
        tables.append({
            "name": COLUMN_NAME,
            "type": COLUMN_TYPE,
            "notNull": IS_NULLABLE == "YES",
            "primaryKey": COLUMN_KEY == "PRI",
            "autoInc": EXTRA == "auto_increment"
        })
    return {"result": tables}


def getCountTables():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor()
    cursor.execute(
        "SELECT "
        "(SELECT COUNT(*) FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_schema = 'abs') AS TableCount, "
        "(SELECT COUNT(*) FROM information_schema.views WHERE table_schema = 'abs') AS ViewCount;")
    result = cursor.fetchone()

    countTables = result[0]
    countViews = result[1]
    db.close()

    return {"result": {"countTables": countTables, "countViews": countViews}}


def setNewTable(newTable: NewTable):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )

    cursor = db.cursor()

    columns_definition = []
    for column in newTable.columns:
        column_def = f"{column.name} {column.type}"
        if column.notNull:
            column_def += " NOT NULL"
        if column.primaryKey:
            column_def += " PRIMARY KEY"
        if column.autoInc:
            column_def += " AUTO_INCREMENT"
        columns_definition.append(column_def)

    create_table_query = f"CREATE TABLE {newTable.name} ({', '.join(columns_definition)})"

    try:
        cursor.execute(create_table_query)
        db.commit()
        return {"result": "success"}
    except mysql.connector.Error as err:
        return {"result": "error", "message": str(err)}
    finally:
        db.close()


def dropTable(table_name):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor()
    try:
        drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
        cursor.execute(drop_table_query)
        db.commit()
        result = {"result": "success", "message": f"Таблица {table_name} успешно удалена."}
    except mysql.connector.Error as err:
        result = {"result": "error", "message": str(err)}
    finally:
        cursor.close()
        db.close()

    return result


def alterTable(tableData: NewTable):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor()
    print(f'tableData.name: {tableData.name}')
    result = {"result": "error", "message": ""}

    try:
        cursor.execute(f"SHOW COLUMNS FROM {tableData.name}")
        existing_columns = {row[0]: row for row in cursor.fetchall()}
        print(f'existing_columns: {existing_columns}')

        new_columns = {column.name: column for column in tableData.columns}

        for column_name, column in new_columns.items():
            if column_name in existing_columns:
                existing_column = existing_columns[column_name]
                if (column.type != existing_column[1] or
                        column.notNull != (existing_column[2] == "NO") or
                        column.autoInc != (existing_column[5] == "auto_increment")):
                    not_null = "NOT NULL" if column.notNull else ""
                    auto_inc = "AUTO_INCREMENT" if column.autoInc else ""
                    column_definition = f"{column.name} {column.type} {not_null} {auto_inc}".strip()
                    alter_table_query = f"ALTER TABLE {tableData.name} MODIFY COLUMN {column_definition}"
                    cursor.execute(alter_table_query)
            else:
                not_null = "NOT NULL" if column.notNull else ""
                auto_inc = "AUTO_INCREMENT" if column.autoInc else ""
                column_definition = f"{column.name} {column.type} {not_null} {auto_inc}".strip()
                alter_table_query = f"ALTER TABLE {tableData.name} ADD COLUMN {column_definition}"
                cursor.execute(alter_table_query)

        print(f'new_columns: {new_columns}')
        for column_name in existing_columns.keys():
            print(f'column_name: {column_name}\n')
            if column_name not in new_columns:
                alter_table_query = f"ALTER TABLE {tableData.name} DROP COLUMN {column_name}"
                cursor.execute(alter_table_query)
                result["message"] += f"Столбец '{column_name}' был удален. "

        db.commit()
        result["result"] = "success"
        result[
            "message"] = f"Столбцы успешно добавлены, изменены или удалены в таблице {tableData.name}. " + result.get(
            "message", "")

    except mysql.connector.Error as err:
        result["message"] = f"Ошибка при добавлении, изменении или удалении столбца: {str(err)}"

    finally:
        cursor.close()
        db.close()

    return result


def getTableValues(tableName: str):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor()
    sql = f'SELECT * FROM `{tableName}`;'
    print(f'sql: {sql}')
    cursor.execute(sql)

    result = cursor.fetchall()
    columns = [column[0] for column in cursor.description]

    data = [dict(zip(columns, row)) for row in result]

    db.close()

    return {"result": data}


def createIndex(indexData: NewIndex):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor()

    sql = f"CREATE INDEX {indexData.index_name} ON {indexData.table_name}({indexData.column_name})"
    print(f'sql: {sql}')

    try:
        cursor.execute(sql)
        db.commit()
        result = "Индекс успешно создан"
    except mysql.connector.Error as err:
        result = f"Ошибка: {err}"

    db.close()
    return {"result": result}


def changeData(data: ChangeData):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor()
    try:
        cursor.execute(f"UPDATE {data.tableName} SET {data.columnName} = %s WHERE id = %s", (data.value, data.stringId))
        db.commit()
        result = "Данные успешно обновлены"
    except mysql.connector.Error as err:
        result = f"Ошибка: {err}"

    db.close()
    return {"result": result}


def fetchData(table_names: List[str], columns: List[str], group_by: List[str] = None,
              conditions: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor()

    base_query = f"SELECT {', '.join(columns)} FROM {', '.join(table_names)}"

    if conditions:
        condition_clauses = [f"{key} = %s" for key in conditions.keys()]
        base_query += " WHERE " + " AND ".join(condition_clauses)

    if group_by: base_query += " GROUP BY " + ", ".join(group_by)

    cursor.execute(base_query, tuple(conditions.values()) if conditions else None)
    results = cursor.fetchall()

    columns = [column[0] for column in cursor.description]

    data = [dict(zip(columns, row)) for row in results]

    db.close()

    return data


def getFirstView():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor()
    sql = f"SELECT column_id, " \
          f"COUNT(*) AS total_tasks, " \
          f"AVG(priority_id) AS average_priority, " \
          f"SUM(CASE WHEN is_done = 1 THEN 1 ELSE 0 END) AS completed_tasks " \
          f"FROM task GROUP BY column_id;"
    cursor.execute(sql)
    result = cursor.fetchall()

    labeled_result = []
    for row in result:
        labeled_result.append({
            "column_id": row[0],
            "total_tasks": row[1],
            "average_priority": row[2],
            "completed_tasks": row[3]
        })

    db.commit()
    db.close()
    return {"result": labeled_result}


def getSecondView(start_date: date, end_date: date):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor()

    sql = f"SELECT id, login, fio, mail, birthday " \
          f"FROM worker " \
          f"WHERE birthday BETWEEN %s AND %s;"

    cursor.execute(sql, (start_date, end_date))
    result = cursor.fetchall()

    labeled_result = []
    for row in result:
        labeled_result.append({
            "id": row[0],
            "login": row[1],
            "fio": row[2],
            "mail": row[3],
            "birthday": row[4]
        })

    db.commit()
    db.close()
    return {"result": labeled_result}


def getThirdView(project_direction_ids: List[int]):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor()

    format_strings = ','.join(['%s'] * len(project_direction_ids))

    sql = f"""
        SELECT p.id, p.name, p.isActive, p.team_id, pd.name 
        FROM project p
        JOIN project_direction pd ON pd.id = p.direction_id
        WHERE p.direction_id IN ({format_strings})
    """

    cursor.execute(sql, tuple(project_direction_ids))
    result = cursor.fetchall()

    labeled_result = []
    for row in result:
        labeled_result.append({
            "id": row[0],
            "name": row[1],
            "isActive": row[2],
            "team_id": row[3],
            "project_direction_name": row[4]
        })

    db.commit()
    db.close()
    return {"result": labeled_result}


def getProjectDirections():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor()

    sql = f"SELECT id, name FROM project_direction"

    cursor.execute(sql)
    result = cursor.fetchall()

    labeled_result = []
    for row in result:
        labeled_result.append({
            "id": row[0],
            "name": row[1],
        })

    db.commit()
    db.close()
    return {"result": labeled_result}


def getColumnNulls(tableName: str, columnName: str):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="abs"
    )
    cursor = db.cursor()

    # Используем форматирование строк для вставки имени таблицы и столбца
    sql = f"SELECT COUNT(*) AS null_count FROM `{tableName}` WHERE `{columnName}` IS NULL;"

    cursor.execute(sql)
    result = cursor.fetchall()

    db.commit()
    db.close()

    return {"result": result[0][0]}