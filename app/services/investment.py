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
    return await session.execute(
        select(model_in)
        .where(model_in.fully_invested == false())
        .order_by(model_in.create_date)
    ).scalars().all()


async def execute_investment_process(
    target: Union[CharityProject, Donation],
    sources: List[Union[CharityProject, Donation]]
) -> Union[CharityProject, Donation]:
    if target is None:
        return target

    available_amount = target.full_amount

    for source in sources:
        if source.fully_invested:
            continue

        need_to_invest = source.full_amount - source.invested_amount
        to_invest = min(need_to_invest, available_amount)

        source.invested_amount += to_invest
        target.invested_amount += to_invest
        available_amount -= to_invest

        if source.full_amount == source.invested_amount:
            source.fully_invested = True
            source.close_date = datetime.now()
        elif available_amount == 0:
            target.fully_invested = True
            target.close_date = datetime.now()
            break

    if target.full_amount == target.invested_amount:
        target.fully_invested = True
        target.close_date = datetime.now()

    return target
