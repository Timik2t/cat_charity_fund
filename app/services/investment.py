from datetime import datetime
from typing import List

from app.models.base import InvestmentAbstract


def investment_process(
        target: InvestmentAbstract,
        sources: List[InvestmentAbstract],
) -> List[InvestmentAbstract]:
    updated_objects = []
    if target.invested_amount is None:
        target.invested_amount = 0
    for source in sources:
        available_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        updated_objects.append(source)
        for investment in [target, source]:
            investment.invested_amount += available_amount
            investment.fully_invested = (
                investment.invested_amount == investment.full_amount
            )
            if investment.fully_invested:
                investment.close_date = datetime.utcnow()
        if target.fully_invested:
            break
    return updated_objects
