from sqlalchemy import Column, String, Text

from app.constants import MAX_CHARITY_PROJECT_NAME, REPRESENTATION_STR_LENGTH

from .base import InvestmentAbstract

REPRESENTATION = (
    'Фонд {name}. {super}'
)


class CharityProject(InvestmentAbstract):
    name = Column(
        String(MAX_CHARITY_PROJECT_NAME),
        unique=True,
        nullable=False
    )
    description = Column(Text)

    def __repr__(self) -> str:
        return REPRESENTATION.format(
            name=self.name[:REPRESENTATION_STR_LENGTH],
            super=super().__repr__(),
        )
