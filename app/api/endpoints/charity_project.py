from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_correct_full_amount_for_update,
    check_name_duplicate,
    check_project_was_closed,
    check_project_was_invested,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import execute_investment_process
router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
) -> List[CharityProjectDB]:
    return await charity_project_crud.get_multiple(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        commit=False,
        object_in=charity_project,
        session=session
    )
    session.add_all(
        execute_investment_process(
            new_charity_project,
            await donation_crud.get_multi_ordered_by_create_date(
                session
            )
        )
    )
    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    object_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    charity_project = await check_charity_project_exists(project_id, session)
    await check_project_was_closed(project_id, session)

    if object_in.full_amount is not None:
        await check_correct_full_amount_for_update(
            project_id, session, object_in.full_amount
        )

    if object_in.name is not None:
        await check_name_duplicate(object_in.name, session)

    return await charity_project_crud.update(
        charity_project,
        object_in,
        session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    charity_project = await check_charity_project_exists(project_id, session)
    await check_project_was_invested(project_id, session)
    return await charity_project_crud.remove(charity_project, session)
