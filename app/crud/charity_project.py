from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate)


class CRUDCharityProject(
    CRUDBase[
        CharityProject,
        CharityProjectCreate,
        CharityProjectUpdate
    ]
):
    async def get_charity_project(
        self,
        object_id: int,
        session: AsyncSession
    ) -> Optional[CharityProject]:
        charityproject_db = await session.execute(
            select(CharityProject).where(
                CharityProject.id == object_id
            )
        )
        return charityproject_db.scalars().first()

    async def get_charity_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        charity_project = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return charity_project.scalars().first()

    async def get_charity_project_close_date(
        self,
        project_id: int,
        session: AsyncSession
    ):
        project_close_date = await session.execute(
            select(CharityProject.close_date).where(
                CharityProject.id == project_id
            )
        )
        return project_close_date.scalars().first()

    async def get_charity_project_invested_amount(
        self,
        project_id: int,
        session: AsyncSession
    ):
        project_invested_amount = await session.execute(
            select(CharityProject.invested_amount).where(
                CharityProject.id == project_id
            )
        )
        return project_invested_amount.scalars().first()


charityproject_crud = CRUDCharityProject(CharityProject)
