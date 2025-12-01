from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Myapp"
    admin_email: str = "email@gmail.com"
    items_per_user: int = 50

settings = Settings()
print(settings)
