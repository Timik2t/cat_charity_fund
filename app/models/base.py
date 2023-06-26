from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base

REPRESENTATION = (
    'Дата создания: {create_date}, '
    'Общая сумма: {full_amount}, '
    'Инвестировано: {invested_amount}, '
    'Дата закрытия: {close_date}. '
)


class InvestmentAbstract(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('invested_amount >= 0', 'invested_amount <= full_amount'),
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime)

    def __repr__(self) -> str:
        return REPRESENTATION.format(
            create_date=self.create_date,
            full_amount=self.full_amount,
            invested_amount=self.invested_amount,
            close_date=self.close_date,
        )
