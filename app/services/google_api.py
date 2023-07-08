from datetime import datetime
from typing import List
from copy import deepcopy
from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject

FORMAT = '%Y/%m/%d %H:%M:%S'

MAX_ROW_COUNT = 100
MAX_COLUMN_COUNT = 10
SPREADSHEET_BODY = dict(
    properties=dict(
        title='Отчет от ',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=MAX_ROW_COUNT,
            columnCount=MAX_COLUMN_COUNT
        )
    ))]
)
TABLE_VALUES = [
    ['Отчет от', ],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
MAX_ROW_COLUMN_COUNT = (
    'Количество строк - {rows_value}, количество столбцов - {columns_value}, '
    'превышает максимально допустимое значение. '
    f'Максимальное количество строк: {MAX_ROW_COUNT}, '
    f'максимальное количество столбцов: {MAX_COLUMN_COUNT}'
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = deepcopy(SPREADSHEET_BODY)
    spreadsheet_body['properties']['title'] += now_date_time
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: List[CharityProject],
    wrapper_services: Aiogoogle
) -> None:

    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = deepcopy(TABLE_VALUES)
    table_values[0].append(now_date_time)
    table_values = [
        *table_values,
        *[list(map(str, [
            project.name,
            project.close_date - project.create_date,
            project.description
        ])) for project in projects]
    ]

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    columns_count = max(map(len, table_values))
    rows_count = len(table_values)
    if (MAX_ROW_COUNT < rows_count or
            MAX_COLUMN_COUNT < columns_count):
        raise ValueError(
            MAX_ROW_COLUMN_COUNT.format(
                rows_value=rows_count,
                columns_value=columns_count,
            )
        )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows_count}C{columns_count}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
