from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.constants import (
    MAX_CHARITY_PROJECT_NAME, MIN_CHARITY_PROJECT_NAME,
    MIN_CHARITY_PROJECT_DESCRIPTION
)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=MIN_CHARITY_PROJECT_NAME,
        max_length=MAX_CHARITY_PROJECT_NAME
    )
    description: Optional[str] = Field(
        None,
        min_length=MIN_CHARITY_PROJECT_DESCRIPTION
    )
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=MIN_CHARITY_PROJECT_NAME,
        max_length=MAX_CHARITY_PROJECT_NAME
    )
    description: str = Field(
        ...,
        min_length=MIN_CHARITY_PROJECT_DESCRIPTION
    )
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: Optional[int]
    create_date: Optional[datetime]
    close_date: Optional[datetime]
    fully_invested: Optional[bool]

    class Config:
        orm_mode = True
