# from typing import Optional

from pydantic import BaseSettings
# EmailStr
DEFAULT_TITLE = 'QRKot'
DEFAULT_DESCRIPTION = 'Благотворительный фонд поддержки усатых-хвостатых'
DEFAULT_SECRET = 'SECRET'


class Settings(BaseSettings):
    app_title: str = DEFAULT_TITLE
    app_description: str = DEFAULT_DESCRIPTION
    database_url: str
    secret: str = DEFAULT_SECRET
    # first_superuser_email: Optional[EmailStr] = None
    # first_superuser_password: Optional[str] = None
    # first_superuser_first_name: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
