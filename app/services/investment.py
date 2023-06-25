from datetime import datetime
from typing import List

from app.models.base import DonationsCharityProjectAbstract


def update_investment(object: DonationsCharityProjectAbstract, amount: int):
    object.invested_amount += amount
    object.fully_invested = (object.invested_amount == object.full_amount)


def execute_investment_process(
    target: DonationsCharityProjectAbstract,
    sources: List[DonationsCharityProjectAbstract],
) -> List[DonationsCharityProjectAbstract]:
    updated_objects = []

    if target.invested_amount is None:
        target.invested_amount = 0

    for source in sources:
        available_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        updated_objects.extend([target, source])
        update_investment(target, available_amount)
        update_investment(source, available_amount)

        if target.fully_invested or source.fully_invested:
            target.close_date = source.close_date = datetime.utcnow()

        if target.fully_invested:
            break

    return updated_objects
