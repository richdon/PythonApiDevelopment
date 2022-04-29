from pydantic import BaseSettings


class Settings(BaseSettings):
    database_port: str
    database_password: str
    database_hostname: str
    database_username: str
    database_name: str
    algorithm: str
    access_token_expire_minutes: int
    secret_key: str

    class Config:
        env_file = '.env'


settings = Settings()
print(settings.database_username)
print(settings.database_password)