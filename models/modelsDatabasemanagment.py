from typing import List

from pydantic import BaseModel
from datetime import date


class NewColumn(BaseModel):
    name: str
    type: str
    notNull: bool
    primaryKey: bool
    autoInc: bool


class NewTable(BaseModel):
    name: str
    columns: List[NewColumn]


class NewIndex(BaseModel):
    table_name: str
    index_name: str
    column_name: str


class ChangeData(BaseModel):
    tableName: str
    columnName: str
    stringId: int
    value: str


class DateRange(BaseModel):
    start_date: date
    end_date: date


class ListNumbers(BaseModel):
    list: List[int]


class Names(BaseModel):
    tableName: str
    columnName: str
