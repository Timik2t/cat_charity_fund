from sqlalchemy import Column, String, Text

from app.core.db import Base, DonationsCharityProjectMixin
from app.constants import MAX_CHARITY_PROJECT_NAME


class CharityProject(Base, DonationsCharityProjectMixin):
    name = Column(
        String(MAX_CHARITY_PROJECT_NAME),
        unique=True,
        nullable=False
    )
    description = Column(Text)
