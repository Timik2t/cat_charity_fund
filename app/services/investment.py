from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.models import CharityProject, Donation


async def get_not_invested_objects(
    model_in: Union[CharityProject, Donation],
    session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    db_objects = await session.execute(
        select(
            model_in
        ).where(
            model_in.fully_invested == false()
        ).order_by(
            model_in.create_date
        )
    )
    return db_objects.scalars().all()


async def close_invested_object(
    obj_to_close: Union[CharityProject, Donation],
) -> None:
    obj_to_close.fully_invested = True
    obj_to_close.close_date = datetime.now()


async def execute_investment_process(
    current_object: Union[CharityProject, Donation],
    session: AsyncSession
):
    if current_object is None:
        return current_object

    db_model = CharityProject if isinstance(current_object, Donation) else Donation
    open_objects = await get_not_invested_objects(db_model, session)
    available_amount = current_object.full_amount

    for open_object in open_objects:
        if open_object.fully_invested:
            continue

        need_to_invest = open_object.full_amount - open_object.invested_amount
        to_invest = min(need_to_invest, available_amount)

        open_object.invested_amount += to_invest
        current_object.invested_amount += to_invest
        available_amount -= to_invest

        if open_object.full_amount == open_object.invested_amount:
            await close_invested_object(open_object)
        elif available_amount == 0:
            await close_invested_object(current_object)
            break

    if current_object.full_amount == current_object.invested_amount:
        await close_invested_object(current_object)

    await session.commit()
    return current_object
