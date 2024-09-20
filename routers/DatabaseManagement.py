from fastapi import APIRouter
from typing import List, Dict, Any
from controllers.DatabaseManagement import getCountTables, getTablesColumns, setNewTable, dropTable, alterTable, \
    getTableColumnsInfo, getTableValues, createIndex, changeData, fetchData, getFirstView, getSecondView, getThirdView, \
    getProjectDirections, getColumnNulls
from models.modelsDatabasemanagment import NewTable, NewIndex, ChangeData, DateRange, ListNumbers, Names

router = APIRouter()


@router.get('/getTablesColumns', tags=["DatabaseManagement"])
def get_tables_columns():
    result = getTablesColumns()
    return result


@router.get('/getCountTables', tags=["DatabaseManagement"])
def get_count_tables():
    result = getCountTables()
    return result


@router.post('/setNewTable', tags=["DatabaseManagement"])
def set_new_table(newTableData: NewTable):
    result = setNewTable(newTableData)
    return result


@router.delete('/dropTable/{tableName}', tags=["DatabaseManagement"])
def drop_table(tableName: str):
    result = dropTable(tableName)
    return result


@router.put('/alterTable', tags=["DatabaseManagement"])
def alter_table(tableData: NewTable):
    result = alterTable(tableData)
    return result


@router.get('/getTableColumnsInfo/{tableName}', tags=["DatabaseManagement"])
def get_table_columns_info(tableName: str):
    result = getTableColumnsInfo(tableName)
    return result


@router.get('/getTableValues/{tableName}', tags=["DatabaseManagement"])
def get_table_values(tableName: str):
    result = getTableValues(tableName)
    return result


@router.post('/setIndex', tags=["DatabaseManagement"])
def set_index(indexData: NewIndex):
    result = createIndex(indexData)
    return result


@router.put('/changeData', tags=["DatabaseManagement"])
def change_data(data: ChangeData):
    result = changeData(data)
    return result


@router.post('/fetchData', tags=["DatabaseManagement"])
def fetch_data(table_names: List[str], columns: List[str], group_by: List[str] = None,
               conditions: Dict[str, Any] = None):
    result = fetchData(table_names, columns, group_by, conditions)
    return result


@router.get('/getFirstView', tags=["DatabaseManagement"])
def get_first_view():
    result = getFirstView()
    return result


@router.post('/getSecondView', tags=["DatabaseManagement"])
def get_second_view(date_range: DateRange):
    result = getSecondView(date_range.start_date, date_range.end_date)
    return result


@router.get('/getProjectDirections', tags=["DatabaseManagement"])
def get_project_directions():
    result = getProjectDirections()
    return result


@router.post('/getThirdView', tags=["DatabaseManagement"])
def get_third_view(project_direction_ids: ListNumbers):
    result = getThirdView(project_direction_ids.list)
    return result


@router.post('/getColumnNulls', tags=["DatabaseManagement"])
def get_column_nulls(names: Names):
    result = getColumnNulls(names.tableName, names.columnName)
    return result
