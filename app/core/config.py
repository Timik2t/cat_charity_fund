from typing import Optional

from pydantic import BaseSettings, EmailStr
from app.constants import DEFAULT_DB_URL
DEFAULT_TITLE = 'QRKot'
DEFAULT_DESCRIPTION = 'Благотворительный фонд поддержки усатых-хвостатых'
DEFAULT_SECRET = 'SECRET'


class Settings(BaseSettings):
    app_title: str = DEFAULT_TITLE
    app_description: str = DEFAULT_DESCRIPTION
    database_url: str = DEFAULT_DB_URL
    secret: str = DEFAULT_SECRET
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
