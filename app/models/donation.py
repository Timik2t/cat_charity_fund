from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import InvestmentAbstract

REPRESENTATION = 'Пожертвование от {user_id}. {super}'


class Donation(InvestmentAbstract):
    user_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=False
    )
    comment = Column(Text)

    def __repr__(self) -> str:
        return REPRESENTATION.format(
            user_id=self.user_id,
            super=super().__repr__(),
        )
