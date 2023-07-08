from http import HTTPStatus

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)

SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'
SPREADSHEET_NOT_UPDATE = (
    'Произошла ошибка при обновлении значений в таблице: {error}'
)

router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
):
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await spreadsheets_update_value(
            spreadsheet_id,
            await charity_project_crud.get_projects_by_completion_rate(
                session
            ),
            wrapper_services
        )
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=SPREADSHEET_NOT_UPDATE.format(error=error)
        )
    return SPREADSHEET_URL.format(spreadsheet_id=spreadsheet_id)
