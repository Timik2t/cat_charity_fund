from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import DonationsCharityProjectAbstract


class Donation(DonationsCharityProjectAbstract):
    user_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable=False
    )
    comment = Column(Text)
