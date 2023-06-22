from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base, DonationsCharityProjectMixin


class Donation(Base, DonationsCharityProjectMixin):
    user_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=False
    )
    comment = Column(Text)
