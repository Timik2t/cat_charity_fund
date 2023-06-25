from http import HTTPStatus

from fastapi import HTTPException
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject

PROJECT_NOT_FOUND = 'Проект не найден!'
PROJECT_EXISTS = 'Проект с таким именем уже существует!'
FORBIDDEN_UPDATE = 'Закрытый проект нельзя редактировать!'
INVESTED_PROJECT_DELETION = (
    'В проект были внесены средства, не подлежит удалению!'
)
INVALID_INVESTED_AMOUNT = (
    'Новая требуемая сумма должна быть больше уже '
    'внесенной в проект суммы - {project_invested_amount}'
)


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        object_id=project_id, session=session
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=PROJECT_NOT_FOUND
        )
    return charity_project


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession
) -> None:
    charity_project_id = await (
        charity_project_crud.get_charity_project_id_by_name(
            project_name=project_name, session=session
        )
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_EXISTS
        )


async def check_project_was_closed(
    project_id: int,
    session: AsyncSession
) -> None:
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=FORBIDDEN_UPDATE
        )


async def check_project_was_invested(
    project_id: int,
    session: AsyncSession
) -> None:
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=INVESTED_PROJECT_DELETION
        )


async def check_correct_full_amount_for_update(
    project_id: int,
    session: AsyncSession,
    full_amount_to_update: PositiveInt
) -> None:
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    if (
        full_amount_to_update and
        full_amount_to_update < charity_project.invested_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=INVALID_INVESTED_AMOUNT.format(
                project_invested_amount=charity_project.invested_amount
            )
        )
