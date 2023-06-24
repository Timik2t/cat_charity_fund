from sqlalchemy import Column, String, Text

from app.constants import MAX_CHARITY_PROJECT_NAME

from .base import DonationsCharityProjectAbstract


class CharityProject(DonationsCharityProjectAbstract):
    name = Column(
        String(MAX_CHARITY_PROJECT_NAME),
        unique=True,
        nullable=False
    )
    description = Column(Text)
